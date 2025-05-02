from datetime import datetime

from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from import_export import admin as import_export_admin
from import_export import fields, resources
from import_export.formats import base_formats
from import_export.forms import ExportForm

from ..common import admin_panel as common_admin_panel
from .models import Data


class CustomExportForm(ExportForm):
    timestamp_from = forms.DateTimeField(
        label=_("Timestamp from (Optional)"),
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    timestamp_to = forms.DateTimeField(
        label=_("Timestamp to (Optional)"),
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[  # Hides the resource field on admin panel UI.
            "resource"
        ].widget = forms.HiddenInput()


class DataResource(resources.ModelResource):
    def __init__(self, **kwargs):
        super().__init__()
        self.timestamp_from = kwargs.get("timestamp_from")
        self.timestamp_to = kwargs.get("timestamp_to")

    full_name = fields.Field(column_name="Full name")
    is_satisfied = fields.Field(column_name="Is satisfied")
    age = fields.Field(column_name="Age")
    created_at = fields.Field(attribute="created_at", column_name="Timestamp")

    class Meta:
        model = Data
        fields = ("full_name", "age", "is_satisfied", "created_at")
        export_order = (
            "full_name",
            "age",
            "is_satisfied",
            "created_at",
        )

    def dehydrate_full_name(self, obj: Data):
        return obj.data["full_name"]

    def dehydrate_age(self, obj: Data):
        return obj.data["age"]

    def dehydrate_is_satisfied(self, obj: Data):
        return obj.data["is_satisfied"]

    def dehydrate_created_at(self, obj: Data):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def filter_export(self, queryset, **kwargs):
        try:
            if self.timestamp_from:
                queryset = queryset.filter(created_at__gte=self.timestamp_from)
        except ValueError:
            pass

        try:
            if self.timestamp_to:
                queryset = queryset.filter(created_at__lt=self.timestamp_to)
        except ValueError:
            pass

        return queryset


class DataAdminForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ("data",)

    def clean_data(self):
        data = self.cleaned_data.get("data")
        required_fields = {
            "full_name": str,
            "is_satisfied": bool,
            "age": int,
        }

        for field, expected_type in required_fields.items():
            if field not in data:
                raise forms.ValidationError(_(f"Missing field '{field}' in JSON data."))
            if not isinstance(data[field], expected_type):
                raise forms.ValidationError(
                    f"Field '{field}' must be of type {expected_type.__name__}"
                )

        return data


@admin.register(Data)
class DataAdmin(import_export_admin.ExportMixin, admin.ModelAdmin):
    resource_classes = (DataResource,)
    export_form_class = CustomExportForm
    form = DataAdminForm
    list_display = ("id", "full_name", "age", "is_satisfied", "created_at")
    search_fields = ("id", "full_name", "age", "is_satisfied", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")

    def id(self, data: Data) -> models.UUIDField:
        return data.data["id"]

    def full_name(self, data: Data) -> str:
        return data.data["full_name"]

    def is_satisfied(self, data: Data) -> bool:
        return data.data["is_satisfied"]

    def age(self, data: Data) -> int:
        return data.data["age"]

    def created_at(self, data: Data) -> datetime:
        return data.created_at

    def get_export_formats(self):
        return (base_formats.XLSX,)

    def get_export_filename(self, request, queryset, file_format):
        def parse_timestamp(timestamp: str) -> str:
            return datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        timestamp_from = request.POST["timestamp_from"]
        timestamp_to = request.POST["timestamp_to"]

        file_name = "Data"
        if timestamp_from:
            try:
                file_name = f"{file_name} from {parse_timestamp(timestamp_from)}"
            except ValueError:
                pass
        if timestamp_to:
            try:
                file_name = f"{file_name} to {parse_timestamp(timestamp_to)}"
            except ValueError:
                pass

        return f"{file_name}.{file_format.get_extension()}"

    def get_export_resource_kwargs(self, request, **kwargs):
        """
        Filter the queryset with additional parameters.
        """

        export_form = kwargs.get("export_form")

        if export_form:
            kwargs.update(timestamp_from=export_form.cleaned_data["timestamp_from"])
            kwargs.update(timestamp_to=export_form.cleaned_data["timestamp_to"])

        return kwargs

    def get_export_data(self, file_format, request, queryset, **kwargs):
        """
        Style the exported data files.
        """

        exported_data = super().get_export_data(
            file_format=file_format, request=request, queryset=queryset, **kwargs
        )

        match type(file_format):
            case base_formats.XLSX:
                exported_data = common_admin_panel.adjust_excel_file(
                    exported_data=exported_data,
                    row_width=20,
                )
            case _:
                pass

        return exported_data

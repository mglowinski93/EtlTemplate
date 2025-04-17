from datetime import datetime

from django import forms
from django.contrib import admin
from django.db import models
from import_export import admin as import_export_admin
from import_export import fields, resources
from django.utils.translation import gettext_lazy as _
from import_export.forms import ExportForm

from .models import Data


class CustomExportForm(ExportForm):
    timestamp_from = forms.DateTimeField(label="timestamp_from")
    timestamp_to = forms.DateTimeField(label="timestamp_to")


class DataResource(resources.ModelResource):
    full_name = fields.Field(column_name="full_name")
    is_satisfied = fields.Field(column_name="is_satisfied")
    age = fields.Field(column_name="age")

    class Meta:
        model = Data
        fields = ("id", "full_name", "is_satisfied", "age", "created_at")
        export_order = (
            "id",
            "full_name",
            "is_satisfied",
            "age",
            "created_at",
        )

    def dehydrate_full_name(self, obj):
        return obj.data["full_name"]

    def dehydrate_is_satisfied(self, obj):
        return obj.data["is_satisfied"]

    def dehydrate_age(self, obj):
        return obj.data["age"]

    def filter_export(self, queryset, **kwargs):
        timestamp_from = kwargs.get("timestamp_from")
        timestamp_to = kwargs.get("timestamp_to")

        try:
            if timestamp_from:
                queryset = queryset.filter(
                    updated_at__gte=datetime.fromisoformat(timestamp_from)
                )
        except ValueError:
            pass

        try:
            if timestamp_to:
                queryset = queryset.filter(
                    updated_at__lt=datetime.fromisoformat(timestamp_to)
                )
        except ValueError:
            pass

        return queryset

class DataAdminForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = "__all__"

    def clean_data(self):
        data = self.cleaned_data.get("data")
        if not isinstance(data, dict):
            raise forms.ValidationError(_("Invalid JSON data."))

        required_fields = {
            "full_name": str,
            "age": int,
            "is_satisfied": bool,
        }

        for field, expected_type in required_fields.items():
            if field not in data:
                raise forms.ValidationError(_(f"Missing field '{field}' in JSON data."))
            if not isinstance(data[field], expected_type):
                raise forms.ValidationError(
                    f"Field '{field}' must be of type {expected_type.__name__}"
                )

        return data





class DataAdmin(import_export_admin.ExportMixin, admin.ModelAdmin):
    resource_class = DataResource
    export_form_class = CustomExportForm


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

    def get_export_resource_kwargs(self, request, **kwargs):
        export_form = kwargs.get("export_form")
        if export_form:
            kwargs.update(timestamp_from=export_form.cleaned_data["timestamp_from"])
            kwargs.update(timestamp_to=export_form.cleaned_data["timestamp_to"])
        return kwargs

admin.site.register(Data, DataAdmin)











    # def get_export_queryset(self, request):
    #     query_set = self.model.objects.all()

    #     timestamp_from = request.GET.get("timestamp_from")
    #     timestamp_to = request.GET.get("timestamp_to")

    #     try:
    #         if timestamp_from:
    #             query_set = query_set.filter(
    #                 updated_at__gte=datetime.fromisoformat(timestamp_from)
    #             )
    #     except ValueError:
    #         pass

    #     try:
    #         if timestamp_to:
    #             query_set = query_set.filter(
    #                 updated_at__lt=datetime.fromisoformat(timestamp_to)
    #             )
    #     except ValueError:
    #         pass

    #     return query_set


from datetime import datetime

from django import forms
from django.contrib import admin
from django.db import models
from import_export import admin as import_export_admin
from import_export import fields, resources
from django.utils.translation import gettext_lazy as _

from .models import Data


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

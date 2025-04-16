from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from import_export import admin as import_export_admin, fields, resources
from .models import Data
from datetime import datetime

class DataResource(resources.ModelResource):
    full_name = fields.Field(column_name='full_name')
    is_satisfied = fields.Field(column_name='is_satisfied')
    age = fields.Field(column_name='age')    
    
    class Meta:
        model = Data
        fields = ('id', 'full_name', 'is_satisfied', 'age', 'created_at', 'updated_at')
        export_order = ('id', 'full_name', 'is_satisfied', 'age', 'created_at', 'updated_at')        

    def dehydrate_full_name(self, obj):
        return obj.data.get('full_name')

    def dehydrate_is_satisfied(self, obj):
        return obj.data.get('is_satisfied')

    def dehydrate_age(self, obj):
        return obj.data.get('age')

@admin.register(Data)
class OutputDataAdmin(import_export_admin.ExportMixin, admin.ModelAdmin):
    resource_class = DataResource
 
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

    def created_at(self, data: Data) -> int:
        return data.created_at

    def get_export_queryset(self, request):
        qs = self.model.objects.all()

        start = request.GET.get("updated_at_start")
        end = request.GET.get("updated_at_end")

        try:
            if start:
                start_date = datetime.strptime(start, "%Y-%m-%d")
                qs = qs.filter(updated_at__gte=start_date)
            if end:
                end_date = datetime.strptime(end, "%Y-%m-%d")
                qs = qs.filter(updated_at__lt=end_date)
        except ValueError:
            pass  # Ignore invalid date inputs

        return qs

    def get_export_resource_kwargs(self, request, *args, **kwargs):
        """
        Remove custom query params (like updated_at_start / end) so import-export doesn't break.
        """
        cleaned_get = request.GET.copy()
        for param in ["updated_at_start", "updated_at_end"]:
            cleaned_get.pop(param, None)
        request.GET = cleaned_get  # mutate it safely
        return super().get_export_resource_kwargs(request, *args, **kwargs)

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
        query_set = self.model.objects.all()

        timestamp_from = request.GET.get("timestamp_from")
        timestamp_to = request.GET.get("timestamp_to")

        try:
            if timestamp_from:
                query_set = query_set.filter(updated_at__gte=datetime.fromisoformat(timestamp_from))
            if timestamp_to:
                query_set = query_set.filter(updated_at__lt=datetime.fromisoformat(timestamp_to))
        except ValueError:
            pass  

        return query_set

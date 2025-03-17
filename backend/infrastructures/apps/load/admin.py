from django.contrib import admin
from django.db import models

from .models import OutputData


@admin.register(OutputData)
class OutputDataAdmin(admin.ModelAdmin):
    data = models.JSONField()
    
    list_display = ("id", "get_full_name", "get_age", "is_satisfied")
    search_fields = ("id", "full_name", "age", "is_satisfied")
    ordering = ("id", "full_name", "age", "is_satisfied")
    readonly_fields = ("id")

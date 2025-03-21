from django.contrib import admin
from django.db import models

from .models import Data


@admin.register(Data)
class OutputDataAdmin(admin.ModelAdmin):
    data = models.JSONField()

    list_display = ("id", "data")
    search_fields = ("id", "data")
    ordering = ("id", "data")
    readonly_fields = ("id",)

from django.contrib import admin
from django.db import models

from .models import OutputData


@admin.register(OutputData)
class OutputDataAdmin(admin.ModelAdmin):
    data = models.JSONField()

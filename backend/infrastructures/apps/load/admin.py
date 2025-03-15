from django.contrib import admin
from .models import OutputData

@admin.register(OutputData)
class OutputDataAdmin(admin.ModelAdmin):
    pass

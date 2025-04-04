from datetime import datetime

from django.contrib import admin

from .models import ExtractHistory


@admin.register(ExtractHistory)
class OutputDataAdmin(admin.ModelAdmin):
    list_display = ("input_file_name", "saved_file_name", "timestamp")

    def input_file_name(self, extract_history: ExtractHistory) -> str:
        return extract_history.input_file_name

    def saved_file_name(self, extract_history: ExtractHistory) -> str:
        return extract_history.saved_file_name

    def timestamp(self, extract_history: ExtractHistory) -> datetime:
        return extract_history.created_at

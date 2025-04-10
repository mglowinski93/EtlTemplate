from django.contrib import admin
from django.db import models

from .models import Data


@admin.register(Data)
class OutputDataAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "age", "is_satisfied")

    def id(self, data: Data) -> models.UUIDField:
        return data.data["id"]

    def full_name(self, data: Data) -> str:
        return data.data["full_name"]

    def is_satisfied(self, data: Data) -> bool:
        return data.data["is_satisfied"]

    def age(self, data: Data) -> int:
        return data.data["age"]

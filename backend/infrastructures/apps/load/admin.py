from django.contrib import admin

from .models import Data


@admin.register(Data)
class OutputDataAdmin(admin.ModelAdmin):
    list_display = ("full_name", "age", "is_satisfied")

    def full_name(self, data: Data):
        return data.data["full_name"]
    
    def is_satisfied(self, data: Data):
        return data.data["is_satisfied"] 

    def age(self, data: Data):
        return data.data["age"]

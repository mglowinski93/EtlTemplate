from django.db import models


# Create your models here.
class OutputData(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    is_satisfied = models.BooleanField()

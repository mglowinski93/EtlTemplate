from django.db import models


class OutputData(models.Model):
    data = models.JSONField()

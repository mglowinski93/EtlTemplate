from django.db import models


class Data(models.Model):
    data = models.JSONField()

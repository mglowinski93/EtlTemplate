import time

from django.db import models


class AutomaticallyTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ManuallyTimestampedModel(models.Model):
    created_at = models.DateTimeField(default=time.time(), editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

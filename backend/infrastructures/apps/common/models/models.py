from django.db import models
from django.utils import timezone


class AutomaticallyTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ManuallyTimestampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now(), editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

from django.db import models

from ..common import models as common_models


class ExtractHistory(common_models.ManuallyTimestampedModel):
    input_file_name = models.CharField(max_length=255)
    saved_file_name = models.CharField(max_length=255)

from django.db import models

from ..common import models as common_models
from modules.extract.domain import value_objects
from django.utils.translation import gettext as _

class ExtractHistory(common_models.ManuallyTimestampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=value_objects.FileId.new,
        editable=False,
        verbose_name=_("ID"),
    )
    input_file_name = models.CharField(max_length=255)
    saved_file_name = models.CharField(max_length=255)

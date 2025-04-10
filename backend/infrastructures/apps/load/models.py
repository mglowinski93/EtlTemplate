from django.db import models
from django.utils.translation import gettext as _

from modules.load.domain import value_objects

from ..common import models as common_models


class Data(common_models.AutomaticallyTimestampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=value_objects.DataId.new,
        editable=False,
        verbose_name=_("ID"),
    )
    data = models.JSONField()

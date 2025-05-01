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
    data = models.JSONField(
        help_text=_(
            'Example: {"full_name": "John Doe", "age": 30, "is_satisfied": true}'
        )
    )

    class Meta:
        verbose_name = _("Data")
        verbose_name_plural = _("Data")

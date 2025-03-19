from django.db import models
from ..common import models as common_models


class Data(common_models.AutomaticallyTimestampedModel):
    data = models.JSONField()

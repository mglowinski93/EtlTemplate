import pytest

from .....common.annotations import YieldFixture
from infrastructures.apps.load import admin
from infrastructures.apps.load.models import Data
from django.contrib import admin as django_admin

@pytest.fixture
def data_admin_panel() -> YieldFixture[admin.DataAdmin]:
    yield admin.DataAdmin(Data, django_admin.site)

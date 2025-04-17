import pytest
from django.contrib import admin as django_admin

from infrastructures.apps.load import admin
from infrastructures.apps.load.models import Data

from .....common.annotations import YieldFixture


@pytest.fixture
def data_admin_panel() -> YieldFixture[admin.DataAdmin]:
    yield admin.DataAdmin(Data, django_admin.site)

import pytest
from django.contrib import admin as django_admin

from infrastructures.apps.load import admin
from infrastructures.apps.load.models import Data

from .....common import annotations
from .....common.conftest import set_test_media_root_directory  # noqa: F401


@pytest.fixture
def data_admin_panel() -> annotations.YieldFixture[admin.DataAdmin]:
    yield admin.DataAdmin(Data, django_admin.site)

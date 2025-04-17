from http import HTTPStatus

from ....dtos import APIClientData
from . import fakers
from infrastructures.apps.load import admin
from django.db import IntegrityError, transaction
from django.http import HttpRequest
from ....utils import get_url
from tests import model_factories
from infrastructures.apps.load.models import Data

def test_saving_new_data(
    unauthenticated_client: APIClientData,
    data_admin_panel: admin.DataAdmin,
):
    # Given
    client = unauthenticated_client.client

    data: Data = model_factories.DataFactory.create()

    form = admin.DataAdminForm(
        data={
            "data": {
                "full_name": data.data["full_name"],
                "age": data.data["age"],
                "is_satisfied": data.data["is_satisfied"],
            },
        }
    )

    with transaction.atomic():
        form.is_valid()
        assert not form.errors
    change = False    

    # When
    data_admin_panel.save_model(
        request=HttpRequest(), obj=data, form=form, change=change
    )

    # Then
    response = client.get(
        get_url(
            path_name="load-detail",
            path_params={"pk": data.id},
        )
    )
    assert response.status_code == HTTPStatus.OK
    assert response.data["full_name"] == data.data["full_name"]




def test_editing_data(
    unauthenticated_client: APIClientData,
    data_admin_panel: admin.DataAdmin,
):
    # Given
    client = unauthenticated_client.client

    data: Data = model_factories.DataFactory.create()
    
    new_full_name = "New Full_Name"
    form = admin.DataAdminForm(
        data={
            "data": {
                "full_name": new_full_name,
                "age": data.data["age"],
                "is_satisfied": data.data["is_satisfied"],
            },
        },
        instance=data
    )

    with transaction.atomic():
        form.is_valid()
        assert not form.errors
    change = True

    # When
    data_admin_panel.save_model(
        request=HttpRequest(), obj=data, form=form, change=change
    )

    # Then
    data.refresh_from_db()
    assert data.data["full_name"] == new_full_name

from http import HTTPStatus

from django.db import transaction
from django.http import HttpRequest

from infrastructures.apps.load import admin
from infrastructures.apps.load.models import Data
from tests import model_factories

from ....dtos import APIClientData, Client
from ....utils import get_url
import csv
import io


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
    data_admin_panel: admin.DataAdmin,
):
    # Given
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
        instance=data,
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


def test_delete_data(
    unauthenticated_client: APIClientData,
    data_admin_panel: admin.DataAdmin,
):
    # Given
    client = unauthenticated_client.client

    data: Data = model_factories.DataFactory.create()

    # When
    data_admin_panel.delete_model(
        request=HttpRequest(), obj=data,
    )

    #Then
    response = client.get(
        get_url(
            path_name="load-detail",
            path_params={"pk": data.id},
        )
    )
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_admin_form_raises_validation_error_when_data_is_not_dict():
    # Given
    form_data = {
        "data": "not a dict"
    }

    # When
    form = admin.DataAdminForm(data={"data": form_data["data"]})

    # Then
    assert not form.is_valid()
    assert "data" in form.errors

def test_admin_form_raises_validation_error_when_age_is_not_a_number():
    # Given
    form_data = {
        "data": {
            "full_name": "John Doe",
            "age": "eleven",  
            "is_satisfied": True
        }
    }

    # When
    form = admin.DataAdminForm(data={"data": form_data["data"]})

    # Then
    assert not form.is_valid()
    assert "data" in form.errors

def test_admin_form_raises_validation_error_when_name_is_not_a_string():
    # Given
    form_data = {
        "data": {
            "full_name": 12345,
            "age": 11,  
            "is_satisfied": True
        }
    }

    # When
    form = admin.DataAdminForm(data={"data": form_data["data"]})

    # Then
    assert not form.is_valid()
    assert "data" in form.errors


def test_admin_form_raises_validation_error_when_name_is_satisfied_is_not_bool():
    # Given
    form_data = {
        "data": {
            "full_name": "John Doe",
            "age": 11,  
            "is_satisfied": "True"
        }
    }

    # When
    form = admin.DataAdminForm(data={"data": form_data["data"]})

    # Then
    assert not form.is_valid()
    assert "data" in form.errors

def test_export_to_excel(
    authenticated_client: Client,
):  
    # Given
    row_number = 5
    for _ in range(row_number): model_factories.DataFactory.create() 
    
    # When
    response = authenticated_client.post(
        get_url(
            path_name="admin:load_data_export",
        ),
            {
                "timestamp_from": "",
                "timestamp_to": "",
                "format": "0",  # CSV format
                "resource": "",
                "_export": "Export",
            }, follow=True
        )

    # Then
    assert response.status_code == HTTPStatus.OK

    rows = list(
        csv.reader(
            io.StringIO(
                response.content.decode("utf-8"))))

    assert len(rows) == row_number + 1 # row with columns included
    expected_headers = ["id","full_name","is_satisfied","age","created_at"]
    assert all(header in rows[0] for header in expected_headers)



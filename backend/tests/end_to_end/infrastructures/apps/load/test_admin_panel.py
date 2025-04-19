import csv
import io
from datetime import timedelta
from http import HTTPStatus

from django.db import transaction
from django.http import HttpRequest
from freezegun import freeze_time

from infrastructures.apps.load import admin
from infrastructures.apps.load.models import Data
from tests import model_factories

from ..... import fakers as common_fakers
from ....dtos import APIClientData, Client
from ....utils import get_url
from . import fakers


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

    new_full_name = common_fakers.fake_full_name()
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
        request=HttpRequest(),
        obj=data,
    )

    # Then
    response = client.get(
        get_url(
            path_name="load-detail",
            path_params={"pk": data.id},
        )
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_admin_form_raises_validation_error_when_age_is_not_a_number():
    # Given
    form_data = fakers.fake_data_form(age="ten")

    # When
    form = admin.DataAdminForm(data={"data": form_data["data"]})

    # Then
    assert not form.is_valid()
    assert "data" in form.errors


def test_admin_form_raises_validation_error_when_name_is_not_a_string():
    # Given
    form_data = fakers.fake_data_form(full_name=12345)

    # When
    form = admin.DataAdminForm(data={"data": form_data["data"]})

    # Then
    assert not form.is_valid()
    assert "data" in form.errors


def test_admin_form_raises_validation_error_when_name_is_satisfied_is_not_bool():
    # Given
    form_data = fakers.fake_data_form(is_satisfied="True")

    # When
    form = admin.DataAdminForm(data={"data": form_data["data"]})

    # Then
    assert not form.is_valid()
    assert "data" in form.errors


def test_export_to_csv(
    authenticated_client: Client,
):
    # Given
    csv_format = "0"
    row_number = 5

    model_factories.DataFactory.create_batch(size=row_number)

    # When
    response = authenticated_client.post(
        get_url(
            path_name="admin:load_data_export",
        ),
        {
            "timestamp_from": "",
            "timestamp_to": "",
            "format": csv_format,
            "resource": "",
            "_export": "Export",
        },
        follow=True,
    )

    # Then
    assert response.status_code == HTTPStatus.OK

    rows = list(csv.reader(io.StringIO(response.content.decode("utf-8"))))
    assert len(rows) == row_number + 1
    assert all(
        column in rows[0]
        for column in ["id", "full_name", "is_satisfied", "age", "created_at"]
    )


def test_export_to_csv_correct_row_exported_for_given_time_range(
    authenticated_client: Client,
):
    # Given
    csv_format = "0"
    timestamp = common_fakers.fake_timestamp()
    with freeze_time(timestamp - timedelta(weeks=1)):
        model_factories.DataFactory.create()

    with freeze_time(timestamp):
        data: Data = model_factories.DataFactory.create()

    with freeze_time(timestamp + timedelta(weeks=1)):
        model_factories.DataFactory.create()

    timestamp_from = timestamp - timedelta(days=1)
    timestamp_to = timestamp + timedelta(days=1)

    # When
    response = authenticated_client.post(
        get_url(
            path_name="admin:load_data_export",
        ),
        {
            "timestamp_from": timestamp_from.isoformat(),
            "timestamp_to": timestamp_to.isoformat(),
            "format": csv_format,
            "resource": "",
            "_export": "Export",
        },
        follow=True,
    )

    # Then
    assert response.status_code == HTTPStatus.OK

    rows = list(csv.reader(io.StringIO(response.content.decode("utf-8"))))
    assert len(rows) == 2
    assert all(str(data.id) in data_row for data_row in rows[1:])

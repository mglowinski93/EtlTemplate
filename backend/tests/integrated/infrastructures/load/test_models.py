import pytest
from django.db import IntegrityError

from .... import model_factories


@pytest.mark.parametrize("field", ("data",))
def test_required_fields_for_data_model_are_not_nullable(field: str):
    # Given
    data = model_factories.DataFactory.create()

    # When and then
    setattr(data, field, None)
    with pytest.raises(IntegrityError):
        data.save()

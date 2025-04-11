from functools import partial
from typing import Any

import factory
from django.contrib.auth import get_user_model

from infrastructures.apps.load import models as load_models

from modules.common import time
from . import fakers

User = get_user_model()


class GenerateDataMixin:
    @classmethod
    def generate_data(cls):
        def convert_dict_from_stub(
            stub: factory.base.StubObject, factory_: factory.Factory
        ) -> dict[str, Any]:
            stub_dict = stub.__dict__

            for key, value in stub_dict.items():
                if isinstance(value, factory.base.StubObject):
                    if key in factory_._meta.declarations and isinstance(
                        factory_._meta.declarations[key], factory.Factory
                    ):
                        factory_ = factory_._meta.declarations[key]

                    stub_dict[key] = convert_dict_from_stub(value, factory_)
                    continue

                if (
                    key
                    in [field.name for field in factory_._meta.model._meta.get_fields()]
                    and factory_._meta.model._meta.get_field(key).choices
                ):
                    stub_dict[key] = next(
                        (
                            _value
                            for key, _value in factory._meta.model._meta.get_field(
                                key
                            ).choices
                            if value == _key
                        ),
                        value,
                    )
                    continue

            return stub_dict

        def dict_factory(factory, **kwargs):
            return convert_dict_from_stub(factory.stub(**kwargs), factory)

        return partial(dict_factory, cls)()

class DataFactory(GenerateDataMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = load_models.Data

    data = factory.LazyFunction(fakers.fake_transformed_data)





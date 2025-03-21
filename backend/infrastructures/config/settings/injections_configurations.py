import inject

from ...apps.load.adapters import units_of_work as load_unit_of_work
from ...apps.load.adapters import repositories as query_load_repositories


def inject_config(binder: inject.Binder):
    binder.bind_to_constructor(
        "data_unit_of_work", load_unit_of_work.DjangoDataUnitOfWork
    )
    binder.bind_to_constructor(
        "query_data_repository", query_load_repositories.DjangoDataQueryRepository
    )


inject.configure(inject_config, once=True)

import inject
from django.conf import settings


from ...apps.load.adapters import repositories as load_repositories
from ...apps.load.adapters import units_of_work as load_unit_of_work

def inject_config(binder: inject.Binder):
    binder.bind_to_constructor(
        "load_data_unit_of_work", load_unit_of_work.DjangoDataUnitOfWork
    )

    binder.bind_to_constructor(
        "load_data_repository", load_repositories.DjangoDataDomainRepository
    )

inject.configure(inject_config, once=True)

import inject
from django.conf import settings


from ...apps.load.adapters import repositories as domain_load_repositories
from ...apps.load.adapters import queries as query_load_repositories
from ...apps.load.adapters import units_of_work as load_unit_of_work


#TODO 6: is this configuration correct? I checked the example and it seems like most of this code is not required in ETL 
def inject_config(binder: inject.Binder):
    binder.bind_to_constructor(
        "save_data_unit_of_work", load_unit_of_work.DjangoDataUnitOfWork
    )

    binder.bind_to_constructor(
        "query_data_repository", query_load_repositories.DjangoDataQueryRepository
    )

inject.configure(inject_config, once=True)

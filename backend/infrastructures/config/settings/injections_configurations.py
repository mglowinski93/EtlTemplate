import inject
from django.conf import settings

#TODO - CONFIGURE CLASSES TO INJECT HERE 

# from infrastructures.common.adapters import task_dispatchers

def inject_config(binder: inject.Binder):
    pass
    # binder.bind_to_constructor(
    #     "users_unit_of_work", user_adapters.DjangoUsersUnitOfWork
    # )

inject.configure(inject_config, once=True)

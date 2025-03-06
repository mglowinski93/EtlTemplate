from modules.todos.domain import ports as domain_ports
from .repositories import (
    DjangoCommentsDomainRepository,
    DjangoPointsDomainRepository,
    DjangoTodosDomainRepository,
)
from ...common.adapters import units_of_work

#TODO 
class DjangoTodosUnitOfWork(
    units_of_work.DjangoUnitOfWork, domain_ports.AbstractTodosUnitOfWork
):
    def __init__(self):
        super().__init__(
            [
                units_of_work.RepositoryData(
                    "comments",
                    DjangoCommentsDomainRepository,
                ),
                units_of_work.RepositoryData(
                    "points",
                    DjangoPointsDomainRepository,
                ),
                units_of_work.RepositoryData(
                    "todos",
                    DjangoTodosDomainRepository,
                ),
            ]
        )

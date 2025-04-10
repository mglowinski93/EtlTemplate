from abc import abstractmethod

from ....common.domain import ports as common_ports
from ....transform.domain import value_objects as transform_value_objects


class AbstractDataDomainRepository(common_ports.AbstractDomainRepository):
    @abstractmethod
    def create(self, data: list[transform_value_objects.OutputData]) -> None:
        """
        :param: Data to save.
        :raises: DatabaseError: Failed to save output data.
        """

        pass

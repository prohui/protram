import abc

import shortuuid


class IdGenerator(abc.ABC):
    """
    id generator
    """

    @abc.abstractmethod
    def next_id(self) -> str:
        raise NotImplementedError


class UUIDIdGenerator(IdGenerator):

    def next_id(self) -> str:
        return str(shortuuid.uuid())

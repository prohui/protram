from __future__ import annotations

from abc import ABC


class DomainObject(ABC):

    @classmethod
    def aggregate_type(cls) -> str:
        return cls.__name__


class ValueObject(ABC):
    pass

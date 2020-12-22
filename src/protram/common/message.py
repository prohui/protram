from __future__ import annotations

import abc
from typing import ClassVar, TypeVar, Type


class MessageBase(abc.ABC):
    """
    Message 基类
    """

    ID: ClassVar[str] = "ID"
    DATE: ClassVar[str] = "DATE"

    def __init__(self, payload: str, headers: dict = None):
        self.payload = payload
        if not headers:
            headers = dict()
        self._headers: dict = headers

    def get_required_header(self, name: str) -> str:
        s = self.headers.get(name)
        if s is None:
            raise KeyError("No such header: " + name + " in this message ")
        else:
            return s

    @property
    def id(self) -> str:
        return self.get_required_header(MessageBase.ID)

    @id.setter
    def id(self, value):
        self._headers[MessageBase.ID] = value

    @property
    def headers(self):
        return self._headers

    def set_payload(self, payload: str):
        self.payload = payload

    def set_headers(self, **kwargs):
        self._headers.update(kwargs)

    def set_header(self, name: str, value):
        if self._headers is None:
            self._headers = dict()
        self._headers[name] = value

    def remove_header(self, key: str):
        del self._headers[key]

    @property
    def date(self):
        return self._headers.get(MessageBase.DATE)

    @date.setter
    def date(self, value):
        self._headers[MessageBase.DATE] = value

    def __str__(self):
        return f'headers:{self.headers},payload:{self.payload},id:{self.id},date:{self.date}'


M = TypeVar('M', bound=MessageBase)


class MessageBuilder:
    _body: str
    _headers: dict

    def __init__(self, body: str, headers: dict = None):
        self._body = body
        if not headers:
            headers = dict()
        self._headers = headers

    @staticmethod
    def with_message(message: M) -> MessageBuilder:
        return MessageBuilder(message.payload, message.headers)

    @staticmethod
    def with_payload(payload: str) -> MessageBuilder:
        return MessageBuilder(payload)

    def with_header(self, name: str, value: str) -> MessageBuilder:
        self._headers[name] = value
        return self

    def with_extra_headers(self, prefix: str, headers: dict) -> MessageBuilder:
        for k, v in headers.items():
            self._headers[prefix + k] = v
        return self

    def build(self, message_class: Type[M]) -> M:
        return message_class(self._body, self._headers)

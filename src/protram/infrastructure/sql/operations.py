from __future__ import annotations

import os

import simplejson as json
import time
from typing import Dict

from sqlalchemy.orm import scoped_session

from . import db


class CommonSqlOperations:

    @staticmethod
    def insert_into_event_table(session: scoped_session,
                                event_id: str,
                                body: str,
                                exchange: str,
                                routing_key: str,
                                aggregate_type: str,
                                aggregate_id: str,
                                event_type: str,
                                headers: Dict[str, str]):
        bg_flag = os.getenv("BG_FLAG", "")
        exchange = exchange
        if bg_flag:
            exchange = f"{bg_flag}_{exchange}"
        ins = db.events.insert().values(
            id=event_id,
            exchange=exchange,
            routing_key=routing_key,
            headers=json.dumps(headers),
            body=body,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            creation_time=int(time.time())
        )

        session().execute(ins)

    @staticmethod
    def insert_into_message_table(session: scoped_session, message_id: str, payload: str, destination: str,
                                  headers: Dict[str, str]):
        """
        插入数据到message表
        :param session:
        :param message_id:
        :param payload:
        :param destination:
        :param headers:
        :return:
        """
        bg_flag = os.getenv("BG_FLAG", "")
        destination = destination
        if bg_flag:
            destination = f"{bg_flag}_{destination}"
        ins = db.messages.insert().values(
            id=message_id,
            headers=json.dumps(headers),
            destination=destination,
            payload=payload,
            creation_time=int(time.time())
        )

        session().execute(ins)

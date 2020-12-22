from __future__ import annotations

from sqlalchemy import *

metadata = MetaData(schema='protram')

messages = Table(
    "message", metadata,
    Column("id", String, primary_key=True),
    Column("headers", String),
    Column("payload", String, nullable=False),
    Column("destination", String, nullable=False),
    Column("published", SMALLINT, default=0),
    Column("creation_time", BIGINT),
    Index("events_published_idx", "published", "id")
)

received_messages = Table(
    "received_messages", metadata,
    Column("consumer_id", String(1000)),
    Column("message_id", String(1000)),
    Column("creation_time", BIGINT),
    PrimaryKeyConstraint("consumer_id", "message_id")
)

offset_store = Table(
    "offset_store", metadata,
    Column("client_name", String(255), nullable=False, primary_key=True),
    Column("serialized_offset", String(255))
)

events = Table(
    "events", metadata,
    Column("id", String(1000), primary_key=True),
    Column("exchange", String(1000)),
    Column("routing_key", String, nullable=False),
    Column("headers", String, nullable=False),
    Column("body", String, nullable=False),
    Column("aggregate_type", String, nullable=False),
    Column("aggregate_id", String, nullable=False),
    Column("event_type", String, nullable=False),
    Column("published", SMALLINT, default=0),
    Column("creation_time", BIGINT),
    Index("events_idx", "exchange", "routing_key", "id"),
    Index("events_idx2", "exchange", "aggregate_type", "aggregate_type", "id"),
    Index("events_published_idx", "published", "id")
)

received_events = Table(
    "received_events", metadata,
    Column("subscriber_id", String(1000)),
    Column("event_id", String(1000)),
    Column("creation_time", BIGINT),
    PrimaryKeyConstraint("subscriber_id", "event_id"),
    UniqueConstraint("subscriber_id", "event_id"),
    Index("received_events_idx", "subscriber_id", "event_id")
)

entities = Table(
    "entities", metadata,

    Column("entity_type", String(1000)),
    Column("entity_id", String(1000)),
    Column("entity_version", String(1000), nullable=False),
    PrimaryKeyConstraint("entity_type", "entity_id"),
    Index("entities_idx", "entity_type", "entity_id")
)

snapshots = Table(
    "snapshots", metadata,
    Column("entity_type", String(1000)),
    Column("entity_id", String(1000)),
    Column("entity_version", String(1000)),
    Column("snapshot_type", String(1000), nullable=False),
    Column("snapshot_json", JSON, nullable=False),
    Column("triggering_events", String(1000)),
    PrimaryKeyConstraint("entity_type", "entity_id", "entity_version")
)

cdc_monitoring = Table(
    "cdc_monitoring", metadata,
    Column("reader_id", String(1000), primary_key=True),
    Column("last_time", BIGINT)
)

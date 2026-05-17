"""Parse timestamped network logs for beaconing analysis."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class NetworkEvent:
    timestamp: datetime
    source_ip: str
    destination_ip: str
    destination_port: int
    protocol: str


def parse_events(path: Path) -> list[NetworkEvent]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = csv.DictReader(handle)
        events = [
            NetworkEvent(
                timestamp=datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")),
                source_ip=row["source_ip"],
                destination_ip=row["destination_ip"],
                destination_port=int(row["destination_port"]),
                protocol=row["protocol"].upper(),
            )
            for row in rows
            if row.get("timestamp")
        ]
    return sorted(events, key=lambda event: event.timestamp)


def parse_many(paths: list[Path]) -> list[NetworkEvent]:
    events: list[NetworkEvent] = []
    for path in paths:
        events.extend(parse_events(path))
    return sorted(events, key=lambda event: event.timestamp)

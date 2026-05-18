"""Analyze interval consistency for repeated outbound traffic."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev

from src.parser import NetworkEvent


@dataclass(frozen=True)
class IntervalProfile:
    source_ip: str
    destination_ip: str
    destination_port: int
    protocol: str
    event_count: int
    first_seen: str
    last_seen: str
    average_interval_seconds: float
    min_interval_seconds: float
    max_interval_seconds: float
    jitter_seconds: float
    consistency: float


def build_interval_profiles(events: list[NetworkEvent]) -> list[IntervalProfile]:
    grouped: dict[tuple[str, str, int, str], list[NetworkEvent]] = {}
    for event in events:
        grouped.setdefault((event.source_ip, event.destination_ip, event.destination_port, event.protocol), []).append(event)

    profiles: list[IntervalProfile] = []
    for (source_ip, destination_ip, destination_port, protocol), group in grouped.items():
        ordered = sorted(group, key=lambda event: event.timestamp)
        if len(ordered) < 3:
            continue
        intervals = [
            (current.timestamp - previous.timestamp).total_seconds()
            for previous, current in zip(ordered, ordered[1:])
        ]
        average = mean(intervals)
        jitter = pstdev(intervals) if len(intervals) > 1 else 0.0
        consistency = max(0.0, 1.0 - (jitter / average if average else 1.0))
        profiles.append(
            IntervalProfile(
                source_ip=source_ip,
                destination_ip=destination_ip,
                destination_port=destination_port,
                protocol=protocol,
                event_count=len(ordered),
                first_seen=ordered[0].timestamp.isoformat(),
                last_seen=ordered[-1].timestamp.isoformat(),
                average_interval_seconds=round(average, 2),
                min_interval_seconds=round(min(intervals), 2),
                max_interval_seconds=round(max(intervals), 2),
                jitter_seconds=round(jitter, 2),
                consistency=round(consistency, 3),
            )
        )
    return sorted(profiles, key=lambda profile: (-profile.consistency, -profile.event_count))

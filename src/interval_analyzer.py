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
    event_count: int
    average_interval_seconds: float
    jitter_seconds: float
    consistency: float


def build_interval_profiles(events: list[NetworkEvent]) -> list[IntervalProfile]:
    grouped: dict[tuple[str, str, int], list[NetworkEvent]] = {}
    for event in events:
        grouped.setdefault((event.source_ip, event.destination_ip, event.destination_port), []).append(event)

    profiles: list[IntervalProfile] = []
    for (source_ip, destination_ip, destination_port), group in grouped.items():
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
                event_count=len(ordered),
                average_interval_seconds=round(average, 2),
                jitter_seconds=round(jitter, 2),
                consistency=round(consistency, 3),
            )
        )
    return sorted(profiles, key=lambda profile: (-profile.consistency, -profile.event_count))

"""Score interval profiles for beaconing behavior."""

from __future__ import annotations

from dataclasses import dataclass

from src.interval_analyzer import IntervalProfile


@dataclass(frozen=True)
class BeaconFinding:
    source_ip: str
    destination_ip: str
    destination_port: int
    protocol: str
    event_count: int
    first_seen: str
    last_seen: str
    average_interval_seconds: float
    jitter_seconds: float
    consistency: float
    score: int
    risk: str
    confidence: str
    reason: str


def score_profile(profile: IntervalProfile) -> BeaconFinding | None:
    score = 0
    reasons: list[str] = []
    if profile.event_count >= 5:
        score += 25
        reasons.append(f"{profile.event_count} repeated outbound events")
    if profile.consistency >= 0.9:
        score += 45
        reasons.append("very consistent callback interval")
    elif profile.consistency >= 0.75:
        score += 25
        reasons.append("moderately consistent callback interval")
    if 30 <= profile.average_interval_seconds <= 600:
        score += 20
        reasons.append(f"average interval is {profile.average_interval_seconds} seconds")

    if score < 50:
        return None
    return BeaconFinding(
        source_ip=profile.source_ip,
        destination_ip=profile.destination_ip,
        destination_port=profile.destination_port,
        protocol=profile.protocol,
        event_count=profile.event_count,
        first_seen=profile.first_seen,
        last_seen=profile.last_seen,
        average_interval_seconds=profile.average_interval_seconds,
        jitter_seconds=profile.jitter_seconds,
        consistency=profile.consistency,
        score=score,
        risk="high" if score >= 80 else "medium",
        confidence="strong" if score >= 80 and profile.consistency >= 0.9 else "moderate",
        reason="; ".join(reasons),
    )


def detect_beacons(profiles: list[IntervalProfile]) -> list[BeaconFinding]:
    findings = [finding for profile in profiles if (finding := score_profile(profile))]
    return sorted(findings, key=lambda finding: (-finding.score, finding.destination_ip))

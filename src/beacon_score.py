"""Score interval profiles for beaconing behavior."""

from __future__ import annotations

from dataclasses import dataclass

from src.interval_analyzer import IntervalProfile


@dataclass(frozen=True)
class BeaconFinding:
    source_ip: str
    destination_ip: str
    destination_port: int
    score: int
    risk: str
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
        score=score,
        risk="high" if score >= 80 else "medium",
        reason="; ".join(reasons),
    )


def detect_beacons(profiles: list[IntervalProfile]) -> list[BeaconFinding]:
    findings = [finding for profile in profiles if (finding := score_profile(profile))]
    return sorted(findings, key=lambda finding: (-finding.score, finding.destination_ip))

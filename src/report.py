"""Generate beaconing traffic reports."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from src.beacon_score import BeaconFinding, detect_beacons
from src.interval_analyzer import IntervalProfile, build_interval_profiles
from src.parser import NetworkEvent, parse_many


def event_to_dict(event: NetworkEvent) -> dict:
    """Return a JSON-friendly network event."""
    return {
        "timestamp": event.timestamp.isoformat(),
        "source_ip": event.source_ip,
        "destination_ip": event.destination_ip,
        "destination_port": event.destination_port,
        "protocol": event.protocol,
    }


def build_summary(events: list[NetworkEvent], profiles: list[IntervalProfile], findings: list[BeaconFinding]) -> dict:
    """Return dashboard-friendly summary data."""
    return {
        "events": len(events),
        "sources": len({event.source_ip for event in events}),
        "destinations": len({event.destination_ip for event in events}),
        "interval_profiles": len(profiles),
        "beacon_findings": len(findings),
        "high_risk": sum(1 for finding in findings if finding.risk == "high"),
        "medium_risk": sum(1 for finding in findings if finding.risk == "medium"),
    }


def build_source_risk(profiles: list[IntervalProfile], findings: list[BeaconFinding]) -> list[dict]:
    """Return source-IP risk rows for triage."""
    rows = []
    sources = {profile.source_ip for profile in profiles} | {finding.source_ip for finding in findings}
    for source_ip in sorted(sources):
        source_profiles = [profile for profile in profiles if profile.source_ip == source_ip]
        source_findings = [finding for finding in findings if finding.source_ip == source_ip]
        rows.append(
            {
                "source_ip": source_ip,
                "profiles": len(source_profiles),
                "findings": len(source_findings),
                "max_risk": "high" if any(finding.risk == "high" for finding in source_findings) else ("medium" if source_findings else "low"),
                "destinations": sorted({profile.destination_ip for profile in source_profiles}),
                "average_consistency": round(
                    sum(profile.consistency for profile in source_profiles) / len(source_profiles),
                    3,
                )
                if source_profiles
                else 0.0,
            }
        )
    order = {"high": 3, "medium": 2, "low": 1}
    return sorted(rows, key=lambda row: (-order[row["max_risk"]], -row["findings"], row["source_ip"]))


def build_report(profiles: list[IntervalProfile], findings: list[BeaconFinding]) -> str:
    sorted_findings = sorted(findings, key=lambda finding: (-finding.score, finding.destination_ip))
    lines = [
        "# Beaconing Traffic Report",
        "",
        f"- Interval profiles: {len(profiles)}",
        f"- Beacon findings: {len(sorted_findings)}",
        f"- High risk: {sum(1 for finding in sorted_findings if finding.risk == 'high')}",
        "",
        "## Priority Queue",
        "",
    ]
    if not sorted_findings:
        lines.append("No immediate analyst queue was generated.")
    for index, finding in enumerate(sorted_findings[:5], start=1):
        lines.append(
            f"{index}. **{finding.risk}** {finding.source_ip} -> "
            f"{finding.destination_ip}:{finding.destination_port} every {finding.average_interval_seconds}s"
        )
    lines.extend(
        [
            "",
            "## Findings",
            "",
        ]
    )
    if not sorted_findings:
        lines.append("No periodic callback behavior was detected.")
    for finding in sorted_findings:
        lines.extend(
            [
                f"### {finding.source_ip} -> {finding.destination_ip}:{finding.destination_port}",
                "",
                f"- Risk: {finding.risk}",
                f"- Confidence: {finding.confidence}",
                f"- Score: {finding.score}",
                f"- Events: {finding.event_count}",
                f"- Window: {finding.first_seen} to {finding.last_seen}",
                f"- Average interval: {finding.average_interval_seconds}s",
                f"- Jitter: {finding.jitter_seconds}s",
                f"- Consistency: {finding.consistency}",
                f"- Why: {finding.reason}",
                "- Recommended next step: Confirm destination ownership, review process telemetry for the source host, and block if unauthorized.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_triage_report(summary: dict, source_risk: list[dict], findings: list[BeaconFinding]) -> str:
    """Return compact analyst triage report."""
    lines = [
        "# Beaconing Traffic Triage",
        "",
        f"- Events analyzed: {summary['events']}",
        f"- Interval profiles: {summary['interval_profiles']}",
        f"- Beacon findings: {summary['beacon_findings']}",
        "",
        "## Source Risk",
        "",
    ]
    for row in source_risk:
        destinations = ", ".join(row["destinations"]) if row["destinations"] else "none"
        lines.append(
            f"- `{row['source_ip']}`: {row['max_risk']}, profiles={row['profiles']}, "
            f"findings={row['findings']}, destinations={destinations}"
        )
    lines.extend(["", "## Analyst Queue", ""])
    if not findings:
        lines.append("- No immediate analyst queue was generated.")
    for finding in sorted(findings, key=lambda item: (-item.score, item.destination_ip))[:8]:
        lines.append(
            f"- `{finding.risk}` {finding.source_ip} -> {finding.destination_ip}:{finding.destination_port}: "
            f"{finding.event_count} events, interval={finding.average_interval_seconds}s, consistency={finding.consistency}"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect periodic outbound beaconing traffic")
    parser.add_argument("logs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, default=Path("reports/beacon-report.md"))
    parser.add_argument("--json-out", type=Path, default=Path("reports/beacon-findings.json"))
    parser.add_argument("--events-out", type=Path, default=Path("reports/events.json"))
    parser.add_argument("--profiles-out", type=Path, default=Path("reports/interval-profiles.json"))
    parser.add_argument("--summary-out", type=Path, default=Path("reports/summary.json"))
    parser.add_argument("--source-risk-out", type=Path, default=Path("reports/source-risk.json"))
    parser.add_argument("--triage-out", type=Path, default=Path("reports/triage.md"))
    args = parser.parse_args()

    events = parse_many(args.logs)
    profiles = build_interval_profiles(events)
    findings = detect_beacons(profiles)
    summary = build_summary(events, profiles, findings)
    source_risk = build_source_risk(profiles, findings)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build_report(profiles, findings), encoding="utf-8")
    args.json_out.write_text(json.dumps([asdict(finding) for finding in findings], indent=2) + "\n", encoding="utf-8")
    args.events_out.write_text(json.dumps([event_to_dict(event) for event in events], indent=2) + "\n", encoding="utf-8")
    args.profiles_out.write_text(json.dumps([asdict(profile) for profile in profiles], indent=2) + "\n", encoding="utf-8")
    args.summary_out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    args.source_risk_out.write_text(json.dumps(source_risk, indent=2) + "\n", encoding="utf-8")
    args.triage_out.write_text(build_triage_report(summary, source_risk, findings), encoding="utf-8")
    print(f"Built {len(profiles)} interval profile(s)")
    print(f"Detected {len(findings)} beacon candidate(s)")


if __name__ == "__main__":
    main()

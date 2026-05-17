"""Generate beaconing traffic reports."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from src.beacon_score import BeaconFinding, detect_beacons
from src.interval_analyzer import IntervalProfile, build_interval_profiles
from src.parser import parse_many


def build_report(profiles: list[IntervalProfile], findings: list[BeaconFinding]) -> str:
    lines = [
        "# Beaconing Traffic Report",
        "",
        f"- Interval profiles: {len(profiles)}",
        f"- Beacon findings: {len(findings)}",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("No periodic callback behavior was detected.")
    for finding in findings:
        lines.extend(
            [
                f"### {finding.source_ip} -> {finding.destination_ip}:{finding.destination_port}",
                "",
                f"- Risk: {finding.risk}",
                f"- Score: {finding.score}",
                f"- Why: {finding.reason}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect periodic outbound beaconing traffic")
    parser.add_argument("logs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, default=Path("reports/beacon-report.md"))
    parser.add_argument("--json-out", type=Path, default=Path("reports/beacon-findings.json"))
    args = parser.parse_args()

    profiles = build_interval_profiles(parse_many(args.logs))
    findings = detect_beacons(profiles)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build_report(profiles, findings), encoding="utf-8")
    args.json_out.write_text(json.dumps([asdict(finding) for finding in findings], indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(profiles)} interval profile(s)")
    print(f"Detected {len(findings)} beacon candidate(s)")


if __name__ == "__main__":
    main()

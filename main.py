"""CLI entrypoint for Beaconing Traffic Detector."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.beacon_score import detect_beacons
from src.interval_analyzer import build_interval_profiles
from src.parser import parse_many
from src.report import build_report, build_source_risk, build_summary, build_triage_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Beaconing traffic detector")
    parser.add_argument("logs", nargs="+", type=Path, help="CSV network log file(s)")
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()

    events = parse_many(args.logs)
    profiles = build_interval_profiles(events)
    findings = detect_beacons(profiles)
    summary = build_summary(events, profiles, findings)
    source_risk = build_source_risk(profiles, findings)
    triage = build_triage_report(summary, source_risk, findings)
    report = build_report(profiles, findings)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (args.out_dir / "source_risk.json").write_text(json.dumps(source_risk, indent=2) + "\n", encoding="utf-8")
    (args.out_dir / "report.md").write_text(report, encoding="utf-8")
    (args.out_dir / "triage.md").write_text(triage, encoding="utf-8")
    print(f"Analysed {summary['events']} event(s), {len(findings)} beacon finding(s)")


if __name__ == "__main__":
    main()

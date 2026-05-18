from pathlib import Path
import unittest

from src.beacon_score import detect_beacons
from src.interval_analyzer import build_interval_profiles
from src.parser import parse_events, parse_many
from src.report import build_report, build_source_risk, build_summary, build_triage_report


ROOT = Path(__file__).resolve().parents[1]


class BeaconingTests(unittest.TestCase):
    def test_detects_periodic_beacon_sample(self) -> None:
        events = parse_events(ROOT / "data/beacon-sample.csv")
        findings = detect_beacons(build_interval_profiles(events))

        self.assertEqual(1, len(findings))
        self.assertEqual("high", findings[0].risk)
        self.assertEqual("strong", findings[0].confidence)
        self.assertEqual(60.0, findings[0].average_interval_seconds)
        self.assertIn("consistent", findings[0].reason)

    def test_normal_network_does_not_alert(self) -> None:
        events = parse_events(ROOT / "data/normal-network.csv")
        self.assertEqual([], detect_beacons(build_interval_profiles(events)))

    def test_report_contains_destination(self) -> None:
        profiles = build_interval_profiles(parse_many([ROOT / "data/beacon-sample.csv"]))
        report = build_report(profiles, detect_beacons(profiles))

        self.assertIn("Beaconing Traffic Report", report)
        self.assertIn("198.51.100.77", report)
        self.assertIn("Recommended next step", report)

    def test_builds_summary_source_risk_and_triage(self) -> None:
        events = parse_many([ROOT / "data/normal-network.csv", ROOT / "data/beacon-sample.csv"])
        profiles = build_interval_profiles(events)
        findings = detect_beacons(profiles)
        summary = build_summary(events, profiles, findings)
        source_risk = build_source_risk(profiles, findings)
        triage = build_triage_report(summary, source_risk, findings)

        self.assertEqual(11, summary["events"])
        self.assertTrue(any(row["source_ip"] == "10.0.0.9" and row["max_risk"] == "high" for row in source_risk))
        self.assertIn("Beaconing Traffic Triage", triage)


if __name__ == "__main__":
    unittest.main()

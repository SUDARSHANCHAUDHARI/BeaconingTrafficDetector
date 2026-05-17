from pathlib import Path
import unittest

from src.beacon_score import detect_beacons
from src.interval_analyzer import build_interval_profiles
from src.parser import parse_events, parse_many
from src.report import build_report


ROOT = Path(__file__).resolve().parents[1]


class BeaconingTests(unittest.TestCase):
    def test_detects_periodic_beacon_sample(self) -> None:
        events = parse_events(ROOT / "data/beacon-sample.csv")
        findings = detect_beacons(build_interval_profiles(events))

        self.assertEqual(1, len(findings))
        self.assertEqual("high", findings[0].risk)
        self.assertIn("consistent", findings[0].reason)

    def test_normal_network_does_not_alert(self) -> None:
        events = parse_events(ROOT / "data/normal-network.csv")
        self.assertEqual([], detect_beacons(build_interval_profiles(events)))

    def test_report_contains_destination(self) -> None:
        profiles = build_interval_profiles(parse_many([ROOT / "data/beacon-sample.csv"]))
        report = build_report(profiles, detect_beacons(profiles))

        self.assertIn("Beaconing Traffic Report", report)
        self.assertIn("198.51.100.77", report)


if __name__ == "__main__":
    unittest.main()

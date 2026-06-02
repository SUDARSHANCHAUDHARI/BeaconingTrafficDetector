# Beaconing Traffic Detector

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#requirements)
[![Status](https://img.shields.io/badge/status-MVP-green)](#status)
[![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#safe-use)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Detects periodic outbound callback (C2 beacon) behavior from timestamped network logs by scoring inter-arrival timing consistency per source/destination pair.

---

## Overview

Beaconing Traffic Detector is a defensive analysis lab tool that parses timestamped CSV network logs, groups repeated outbound traffic by source/destination/port, and scores how "periodic" each pattern is. High-confidence periodic callbacks — the signature of command-and-control beaconing — are flagged with a risk level and timing-window context. Outputs include Markdown reports, source risk JSON, interval profiles, and an analyst triage handoff.

## Features

- Parses timestamped network CSV logs
- Groups repeated outbound traffic by source, destination, and port
- Calculates interval jitter and consistency per profile
- Scores suspicious periodic callbacks with confidence and risk
- Adds timing-window and source-risk context
- Outputs Markdown report, triage handoff, interval profile JSON, source risk JSON, and findings JSON

## Requirements

- Python 3.10 or newer
- Linux, macOS, or Windows
- No third-party Python packages (standard library only)
- Optional: Docker for the demo container

## Installation

```bash
git clone https://github.com/SUDARSHANCHAUDHARI/BeaconingTrafficDetector.git
cd BeaconingTrafficDetector
pip install .
```

This registers the `beaconing-detector` CLI command.

To run without installing:

```bash
python3 main.py --help
```

## Usage

Analyze the included sample network logs:

```bash
python3 main.py data/normal-network.csv data/beacon-sample.csv --out-dir reports
```

Generated outputs in `reports/`:

- `summary.json` — counts, sources, findings
- `source_risk.json` — per-source risk table
- `report.md` — Markdown beaconing detection report
- `triage.md` — analyst triage checklist

## Project Structure

```
BeaconingTrafficDetector/
├── src/            Parser, interval analyzer, beacon scorer, report builder
├── data/           Safe sample network logs (normal + beacon)
├── reports/        Example generated output
├── docker/         Dockerfile + compose support
├── docs/           Architecture, security notes, demo
├── tests/          Unit tests
├── main.py         CLI entrypoint
├── pyproject.toml  Package metadata
└── LICENSE
```

## Testing

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Docker Demo

```bash
docker compose run --rm beaconing-demo
```

## Safe Use

This project is defensive and analysis-focused. Use only with logs, systems, and lab environments you own or have explicit written permission to assess. The included sample logs are synthetic and safe for public demo use.

## Status

Working CLI MVP with tests, sample data, and Docker support.

## Roadmap

- Support pcap and JSONL log input
- Configurable interval window and jitter thresholds
- Allowlist for known periodic services (NTP, telemetry)
- Visualization of beacon timing distributions
- GitHub release `v0.1.0-mvp`

## License

Released under the [MIT License](LICENSE). You are free to use, modify, and distribute this software with attribution.

## Author

**Sudarshan Chaudhari** — [SudarshanTechLabs](https://github.com/SUDARSHANCHAUDHARI)
Bangkok, Thailand

For inquiries: open an issue on [GitHub](https://github.com/SUDARSHANCHAUDHARI/BeaconingTrafficDetector/issues).

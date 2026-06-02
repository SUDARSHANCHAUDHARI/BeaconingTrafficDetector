# Beaconing Traffic Detector

[![Python](https://img.shields.io/badge/Python-3.12-blue)](#) [![Status](https://img.shields.io/badge/status-MVP-green)](#) [![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#)

Lab tool that detects periodic outbound callback behavior from timestamped network logs.

- **Portfolio group:** Cybersecurity lab project
- **Status:** MVP implemented, tested, committed, and pushed to GitHub
- **GitHub:** https://github.com/SUDARSHANCHAUDHARI/BeaconingTrafficDetector
- **Local path:** `/Users/screencloudsudarshan/SUDARSHAN_CODE/sudarshan_repos/CyberSecurity/BeaconingTrafficDetector`

## MVP Snapshot

This repository includes a working MVP with safe sample data, deterministic detection or analysis logic, local tests, and generated output reports where relevant. It is ready for README/demo polish or deeper product work.

## Safe Use

This project is defensive and analysis-focused. Use only with logs, systems, repositories, and lab environments you own or have permission to assess.

## Core Features

- detect periodic outbound traffic
- calculate interval consistency
- score suspicious behavior
- show graph/table


## Install

```bash
pip install .
```

This registers the `beaconing-detector` command. Or run directly:

```bash
python3 main.py --help
```

## Quick Start

```bash
python3 -m src.report data/normal-network.csv data/beacon-sample.csv
python3 -m unittest discover -s tests -p 'test_*.py'
```

## MVP Capabilities

- Parses timestamped network CSV logs
- Groups repeated outbound traffic by source, destination, and port
- Calculates interval jitter and consistency
- Scores suspicious periodic callbacks
- Adds confidence, timing window, and source-risk context
- Writes Markdown report, triage handoff, interval profile JSON, source risk JSON, and findings JSON

## Demo Artifacts

- [Architecture](docs/ARCHITECTURE.md)
- [Security notes](docs/SECURITY_NOTES.md)
- [Demo walkthrough](docs/DEMO.md)
- [Release notes](docs/RELEASE_NOTES.md)
- [Sample beacon report](reports/beacon-report.md)
- [Sample triage report](reports/triage.md)
- [Sample source risk table](reports/source-risk.json)

## Docker Demo

```bash
docker compose run --rm beaconing-demo
```

## Roadmap

- Add allowlist/suppression support for known polling services.
- Add configurable interval ranges and minimum event counts.
- Add protocol-aware scoring for DNS, HTTPS, and unusual ports.
- Add dashboard charts for interval consistency.
- Prepare GitHub release `v0.1.0-mvp`.

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
- Writes Markdown and JSON reports

## Roadmap

- Polish sample output screenshots or terminal demos
- Add architecture diagram and deeper implementation notes
- Expand test coverage around edge cases
- Add Docker or local demo workflow where useful
- Prepare `v0.1.0-mvp` release notes

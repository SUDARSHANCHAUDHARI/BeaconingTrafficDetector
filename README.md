# Beaconing Traffic

**Goal:** Detect periodic malware-like callback traffic.

**MVP:** Analyze timestamped network logs for repeated intervals.

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

## Repository Status

This repository contains a working Beaconing Traffic Detector MVP with safe sample traffic, interval scoring, generated reports, and tests.

## Production Foundation

- Private GitHub repository linked to `main`
- Initial MVP scaffold committed
- CI repository-health workflow
- Security policy
- Contribution guide
- Pull request and issue templates
- Production readiness checklist
- Safe ignore rules for local secrets and generated files

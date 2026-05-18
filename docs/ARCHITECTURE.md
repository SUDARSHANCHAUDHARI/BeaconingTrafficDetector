# Architecture

Beaconing Traffic Detector is a defensive lab for identifying periodic outbound callback behavior from timestamped network logs.

```mermaid
flowchart LR
  Logs["network CSV logs"] --> Parser["CSV parser"]
  Parser --> Events["Normalized events JSON"]
  Events --> Profiles["Interval profiles"]
  Profiles --> Scoring["Beacon scoring"]
  Scoring --> Findings["Findings JSON"]
  Profiles --> SourceRisk["Source risk JSON"]
  Findings --> Report["Markdown report"]
  Findings --> Triage["Triage handoff"]
```

## Current MVP

- Parses timestamped network CSV logs.
- Groups outbound traffic by source, destination, port, and protocol.
- Calculates average interval, min/max interval, jitter, and consistency.
- Scores periodic callback behavior and assigns confidence.
- Emits events, interval profiles, summary, source risk, findings, report, and triage artifacts.

## Future Product Shape

- Configurable scoring by protocol and expected polling patterns.
- Allowlist and suppression workflow for known SaaS or telemetry services.
- Dashboard charts for interval consistency and source/destination timelines.

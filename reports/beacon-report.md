# Beaconing Traffic Report

- Interval profiles: 2
- Beacon findings: 1
- High risk: 1

## Priority Queue

1. **high** 10.0.0.9 -> 198.51.100.77:443 every 60.0s

## Findings

### 10.0.0.9 -> 198.51.100.77:443

- Risk: high
- Confidence: strong
- Score: 90
- Events: 6
- Window: 2026-05-18T14:00:00+00:00 to 2026-05-18T14:05:00+00:00
- Average interval: 60.0s
- Jitter: 0.0s
- Consistency: 1.0
- Why: 6 repeated outbound events; very consistent callback interval; average interval is 60.0 seconds
- Recommended next step: Confirm destination ownership, review process telemetry for the source host, and block if unauthorized.

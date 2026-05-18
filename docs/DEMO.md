# Demo

Run the included normal and beacon-like network logs:

```bash
python3 -m src.report data/normal-network.csv data/beacon-sample.csv
```

Expected output:

```text
Built 2 interval profile(s)
Detected 1 beacon candidate(s)
```

Generated artifacts:

- `reports/events.json`
- `reports/interval-profiles.json`
- `reports/summary.json`
- `reports/source-risk.json`
- `reports/beacon-findings.json`
- `reports/beacon-report.md`
- `reports/triage.md`

The sample demonstrates a strong 60-second HTTPS callback pattern from `10.0.0.9` to `198.51.100.77`.

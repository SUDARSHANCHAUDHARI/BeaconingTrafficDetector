# Production Readiness

## Current Status

This repository has a working local MVP with deterministic network-log parsing, safe sample data, generated reports, and tests. It is not production complete yet.

## Required Before Public Release

- Add log size limits and streaming parsing before hosted uploads.
- Validate CSV schema and report parse errors without stopping whole-file analysis.
- Add structured logging without leaking secrets.
- Add allowlist/suppression workflow for known polling services.
- Add authentication and authorization before storing multi-user logs.
- Add retention controls for uploaded network logs and generated reports.
- Run dependency and secret scans before release.

## Definition of Done

- CI passes on pull requests.
- README has setup, usage, and security notes.
- Sample data is safe to publish.
- Error paths are handled clearly.
- No secrets or local machine paths are committed.

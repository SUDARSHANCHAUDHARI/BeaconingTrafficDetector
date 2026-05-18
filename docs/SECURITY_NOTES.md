# Security Notes

This project is defensive and analysis-only. Use it only with network logs from systems and networks you own or have permission to monitor.

## Data Handling

- Network logs can expose internal IPs, public destinations, ports, protocols, and timing.
- Redact private host mappings and sensitive destinations before sharing reports.
- Do not commit production network telemetry.
- Sample data uses documentation IP ranges and synthetic internal addresses.

## Detection Caveats

- Periodic traffic is not automatically malicious.
- Software updates, health checks, signage polling, monitoring agents, and SaaS clients can create regular intervals.
- Treat findings as triage leads and correlate with process, DNS, proxy, and endpoint telemetry.

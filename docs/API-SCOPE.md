# Network API — M0 scope

## Planned endpoints (not yet implemented)
- `GET /v1/dns/lookup` — DNS record lookup
- `GET /v1/rdap/domain` — RDAP domain data
- `GET /v1/ip/lookup` — IP metadata
- `GET /v1/http/check` — bounded HTTP diagnostics
- `GET /v1/tls/check` — certificate metadata and validation
- `GET /healthz` — service liveness

## Shared response contract
JSON with request ID, result or structured error, execution duration, and usage accounting metadata. Use explicit versioning and consistent pagination where needed.

## Abuse controls
Public targets only; reject forbidden IP ranges after DNS resolution and on redirects. Explicit allowed schemes and ports. Per-request timeouts, response caps, tenant quotas, concurrency limits and audit logs. Protect against DNS rebinding and IPv4/IPv6 bypasses. Restrict RDAP outbound destinations to trusted registry/bootstrap targets.

## Testing
Offline fixtures for DNS, RDAP, TLS and HTTP; property-based validation tests; SSRF regression cases; no external network dependency in CI.

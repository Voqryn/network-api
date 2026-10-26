# Voqryn Network API — Agent Instructions

Implement versioned, documented, testable DNS, RDAP, IP, HTTP and TLS diagnostic endpoints.

## Security requirements
- Block SSRF, loopback, private, link-local, multicast and cloud metadata destinations; validate every redirect and resolved address.
- Enforce timeouts, response size limits, rate limits and per-tenant quotas.
- Avoid open proxies, unrestricted port scanning and arbitrary network access.
- Never log secrets or sensitive request contents.
- Use fixtures/mocks in CI rather than depending on live external endpoints.

## M0 scope
API contracts, threat model, fixtures and a minimal health endpoint before external network queries.

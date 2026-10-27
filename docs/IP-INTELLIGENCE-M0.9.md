# M0.9 — resilient optional IP enrichment

IP Check's core IP/version response must remain available if local enrichment data is absent, corrupt or unreadable. The `/v1/ip/me/details` endpoint now returns `intelligence.available=false` on expected dataset errors and logs the failure. Never substitute guessed location or ASN data.

Security: The endpoint uses the ASGI request peer and accepts no arbitrary IP query parameter. Accurate public client IPs require a verified trusted-proxy deployment. Spoofed forwarding headers must not be accepted from untrusted clients; test the full proxy chain in staging.

Tests added for failure fallback and spoofed-header behavior at the application layer. CI and live proxy behavior still require verification. Dataset vendor, license, freshness and automation remain undecided.

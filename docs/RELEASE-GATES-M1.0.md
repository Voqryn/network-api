# Voqryn IP Check — M1.0 release gates

**Status:** source changes committed; no deployment or CI pass verified.

1. Network API CI: install package with test extras, compile Python modules, run full pytest suite. Inspect failures before release.
2. Frontend CI: Vite build must contain `dist/tools/my-ip/index.html`; confirm `/v1/ip/me/details` is reachable through the chosen reverse proxy.
3. Test IPv4 and IPv6 from real external clients; check IP family and reported address. Browser requests only report the family actually used.
4. Test injected `X-Forwarded-For`, `Forwarded`, and `X-Real-IP` through the public ingress. The reported IP must not be the spoofed value.
5. Confirm backend only binds loopback, firewall prevents direct external access, TLS works, and logs/privacy retention are documented.
6. Confirm malformed/missing enrichment datasets do not break basic IP checks; no external enrichment calls.
7. Review commercial dataset licensing and attribution before enabling data updates. No vendor chosen.

**Do not call the service production-ready until all gates have evidence.**

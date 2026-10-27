# M0.8 — indexed prefix lookup

The local JSON dataset is loaded into an in-memory dictionary keyed by IP family, prefix length and network address. Queries check at most 33 IPv4 or 129 IPv6 prefix lengths, selecting the longest match. The implementation does not perform network calls.

The importer still limits datasets to 100000 networks and 20 MiB. Loading and validating a large JSON file still costs startup memory and time. This is not yet a production-scale geolocation solution. Data provenance, licensing, automated updates, freshness monitoring and deployment validation remain unresolved.

Potential providers to evaluate separately: MaxMind GeoLite2, DB-IP and IPinfo. Do not assume any license permits use in a public commercial API or website until terms are reviewed. No provider has been selected or integrated.

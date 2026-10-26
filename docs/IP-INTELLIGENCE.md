# IP Intelligence M0.5 — offline-first prototype

The API may optionally enrich the requesting visitor's public IP using a locally installed JSON dataset. No external enrichment API is called, and no IP is stored by the enrichment module.

**Default:** no dataset configured; the response says `available: false`. Never manufacture a country, ASN, provider or VPN status.

Set `VOQRYN_IP_DATASET` to a reviewed local JSON file containing entries such as:

```json
[{"network":"8.8.8.0/24","country":"US","asn":15169,"provider":"Example provider label"}]
```

The example is illustrative, not an authoritative maintained dataset. The operator must source and license a legitimate dataset, validate update frequency and attribution requirements, and ensure data quality before launch. The lookup selects the most-specific matching prefix; private and non-global addresses are not enriched. Changes to the dataset require a process restart or cache clear. Large datasets should eventually use an indexed database instead of linear scans.

**Privacy:** no third-party request, no IP enrichment persistence. Reverse proxy and access logs are separate concerns. Do not label IPs as VPN/proxy/Tor without a defensible dedicated source.

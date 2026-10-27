# M0.7 — staged IP data update pipeline

Status: implemented and committed, not deployed or verified in CI.

The pipeline is **vendor-neutral** and never downloads from the internet. A human/operator must first confirm dataset licensing for commercial use, then stage the file and independently obtain a trusted SHA-256 checksum.

```sh
python -m voqryn_network_api.ip_dataset_pipeline \\
  --source /var/lib/voqryn/staging/ip.json \\
  --destination /var/lib/voqryn/ip-dataset.json \\
  --sha256 YOUR_TRUSTED_SHA256 --dry-run
```

After checking output, repeat without `--dry-run`. Installation is atomic. Restart the API after successful import because the current dataset reader caches records in memory.

**Important:** A hash computed from the same untrusted downloaded file only detects accidental changes; it does not authenticate the provider. Obtain checksums via a trusted authenticated channel or signed manifest. Keep source data licensing and attribution records. The current importer has a 100000-prefix and 20 MiB input limit and uses linear lookups; this is a prototype, not a production-scale geolocation database.

Next: evaluate licensed local databases and indexed lookup formats, then add provider-specific downloads with verified provenance and update scheduling. Do not schedule imports until that decision is made.

# IP dataset update process — M0.6

**No vendor selected and no download configured.** Updates are currently explicit and local only. This prevents silently accepting unlicensed or untrusted datasets.

1. Obtain a dataset from a provider whose license permits Voqryn's intended commercial service and redistribution/display of derived fields.
2. Convert it offline into a bounded JSON array with `network`, `country` (ISO alpha-2), `asn` (integer), and `provider` (string).
3. Run `python -m voqryn_network_api.ip_dataset_update --source /path/to/staged.json --destination /var/lib/voqryn/ip-dataset.json` as an authorized operator.
4. Set `VOQRYN_IP_DATASET=/var/lib/voqryn/ip-dataset.json` for the API service and restart it to refresh its in-memory cache.
5. Validate representative IPv4 and IPv6 results and verify that private/non-global IPs are not enriched.

The importer validates input and atomically replaces the destination only on success. It does **not** download, schedule updates, or refresh running API processes. Automating ingestion requires choosing a licensed provider, authenticated transport, integrity checks, update monitoring and rollback policy.

The JSON lookup is linear and limited to 100000 networks; use an indexed local database for larger real-world datasets.

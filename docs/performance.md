# Performance notes

Measured on Redmi Turbo 3 / Android 16. The public phone source already includes readiness polling, compact snapshots, HTTPS reuse and batching. Release 0.0.2 packages the matching relay; it claims no new speedup over the 0.0.1 phone source.

- Settings UI read: before [1240, 1291, 1238] ms; after [303, 293, 357] ms. Median 1240 → 303 ms.
- Warm HTTPS request median: 300 → 118 ms, excluding the first connection.
- Measured JSON: 4778 → 3063 bytes; visible nodes 31 → 23.
- Two Settings batches, nine operations: 4588 + 6435 = 11023 ms total tool time. Model reasoning between calls is excluded.

This is not an SMS-send benchmark, end-to-end assistant latency, a guarantee for other networks/apps, or a test of the additional focused-field and Recents changes. No real SMS was sent for these measurements.

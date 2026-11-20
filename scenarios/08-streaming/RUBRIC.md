# RUBRIC: Clickstream streaming pipeline

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| Ingestion and partitioning | 4 | Durable append-only log with stable partition key and explicit per-key ordering scope. | Direct producer-to-processor calls or global ordering assumed without mechanism. |
| Windowing and event time | 4 | Event-time windows with watermark, allowed lateness, and window/key aggregate identity. | Processing-time only or late events silently dropped. |
| Backpressure and hot keys | 4 | Consumer-lag signals, bounded buffers, scaling/shedding rule, and hot-key mitigation. | Unbounded queue or no answer for a hot partition. |
| Replay and schema evolution | 4 | Raw retention, idempotent replay writes, versioned schemas, and compatibility rule. | Replay duplicates results or breaking changes allowed silently. |
| Plan-only validation | 4 | Synthetic duplicate/late/replay checks plus `terraform plan`; no live stream or client data. | Validation requires a live streaming service or omits replay/schema checks. |

Total: 20 points.

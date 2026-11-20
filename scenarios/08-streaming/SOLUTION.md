# SOLUTION: Clickstream streaming pipeline

## Model solution

Ingest clicks into a durable append-only log partitioned by session or tenant ID. A stream processor uses event time with a watermark and allowed lateness to compute tumbling or session windows. Raw events are retained in a separate store for replay. Consumer lag drives scaling and bounded buffers; a hot key is salted and re-aggregated. A schema registry checks additive versus breaking changes before producers deploy.

Provider mapping, using generic names elsewhere: AWS uses Kinesis or managed Kafka, functions or Flink, and object storage; Azure uses Event Hubs, Stream Analytics or Flink, and Data Lake storage; GCP uses Pub/Sub, Dataflow, and Cloud Storage or BigQuery.

## Rationale

- An append-only log decouples producers from processors and preserves the source of truth.
- Per-key partitioning gives useful ordering without demanding global order.
- Event-time windows with lateness produce stable aggregates despite network delays.
- Raw retention enables replay after a bug without asking clients to resend.
- Idempotent sink writes make replay safe even under at-least-once delivery.
- Backpressure based on lag protects the pipeline from unbounded queues.
- Schema compatibility checks prevent a producer change from silently breaking consumers.

## Architecture

```
Web/mobile -> ingestion gateway -> append-only log (partition key: session/tenant)
                                      |-> raw retained store (replay source)
                                      v
                              stream processor
                              - event time + watermark
                              - tumbling/session windows
                              - idempotent upsert by window + key
                                      |
                                      v
                              curated topic -> analytics store

Cross-cutting: schema registry + compatibility check, consumer lag metrics,
               bounded buffers, hot-key salting and second-stage aggregation
```

## Trade-offs

- Longer raw retention improves replay but raises storage cost.
- Session windows model behavior better but require more state than tumbling windows.
- Salting fixes hot keys but adds a second aggregation stage.
- Strict schema rules prevent breakage but slow producer changes.
- At-least-once plus idempotent sinks is portable but more work than relying on provider exactly-once claims.
- Sampling reduces load but loses fidelity for rare events.

## Failure modes

- Hot partition from one key saturates a single consumer.
- Late events dropped because watermark or allowed lateness is too aggressive.
- Replay duplicates aggregates because the sink uses append-only writes.
- Breaking schema change makes older consumers fail or misinterpret fields.
- Consumer lag grows without bound and buffers exhaust memory.
- Window state lost on restart, so counts restart from zero.
- Clock skew in producers distorts event-time windows.

## Local validation only

- Publish synthetic events with duplicate IDs and out-of-order timestamps to the emulator.
- Confirm one aggregate per window/key after a local replay using idempotent upserts.
- Show per-key ordering and demonstrate how a hot key is salted and re-aggregated.
- Validate schema versions locally by accepting an additive field and rejecting a breaking type change in notes or a local check.
- Run `terraform plan` and verify log partitions where configurable, retention, raw-store access, schema settings, and consumer permissions.
- Do not connect real clients, start managed jobs, or create cloud storage buckets.

## Note

Replay is only useful if the sink write is idempotent and the raw events were retained before processing.

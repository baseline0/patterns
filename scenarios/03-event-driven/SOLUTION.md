# SOLUTION: Event-driven order ingress

## Model solution

The ingress API validates an order and appends it to a durable queue or topic partitioned by order ID. Consumers process messages idempotently using an event ID recorded atomically with the business change. Failed messages retry with backoff and jitter, then move to a dead-letter queue. A second topic can fan out accepted orders to independent subscribers such as analytics or notification.

Provider mapping, using generic names elsewhere: AWS uses API Gateway, SQS or SNS, Lambda or event buses, and a table store; Azure uses HTTP Functions or API Management, Service Bus queues and topics, Functions, and Cosmos DB; GCP uses API Gateway, Pub/Sub, Cloud Run or Functions, and Firestore.

## Rationale

- A durable log absorbs bursts and decouples ingress from downstream latency.
- Partitioning by order ID preserves per-order order while allowing different orders to process in parallel.
- At-least-once delivery is expected; idempotency keys prevent duplicate side effects.
- DLQs isolate poison messages and keep a backlog from being silently retried forever.
- Schema versioning lets consumers evolve without ambiguous payloads.
- Metrics for age, depth, retries, and DLQ count make backlog risk visible.

## Architecture

```
Client -> ingress API -> validate + assign event ID -> queue/topic (partition key: orderId)
                                                  |-> consumer: inventory (dedupe store)
                                                  |-> consumer: payment  (dedupe store)
                                                  |-> topic: order-accepted -> notification, analytics
                                                  `-> retry with backoff -> DLQ after limit

Observability: queue depth, oldest message age, retry count, DLQ depth, schema version
```

## Trade-offs

- Topic fan-out gives independence but duplicates storage and delivery; a queue gives one consumer group per message.
- Strict per-key ordering limits parallelism for that key.
- Longer retry delays protect downstreams but increase order latency.
- Long DLQ retention aids debugging but increases storage cost.
- Batch processing improves throughput but can complicate per-message idempotency.

## Failure modes

- Duplicate reservation or charge because the consumer committed before recording the event ID.
- Events for one order processed out of order across partitions.
- Poison message retried forever and blocking a partition.
- DLQ accumulates with no owner or replay procedure.
- Visibility timeout shorter than processing time, causing overlapping deliveries.
- Schema drift makes an older consumer misread a new field.
- Success acknowledged before the transaction commits.

## Local validation only

- Publish the same event ID twice and confirm one business effect and one dedupe record.
- Force a consumer failure until the retry limit is reached and confirm the message lands in the DLQ.
- Publish several events for one order and confirm per-key ordering; use different keys to show parallelism.
- Replay a DLQ message into a clean local consumer and confirm no duplicate effect.
- Run `terraform plan` and verify queue/topic type, partitions where configurable, retention, redrive policy, subscriptions, and least-privilege permissions.
- Do not publish to a real topic or start cloud-hosted consumers.

## Note

The dedupe record and the business write must commit together. If they are separate, a crash between them recreates the duplicate problem.

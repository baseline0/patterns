# HINTS: Event-driven order ingress

## Progressive hints

1. Accept the order quickly at the ingress boundary; do not make the client wait for inventory or payment work.
2. Put a durable queue or topic between ingress and processing so producers never call consumers synchronously.
3. Use a queue when one worker group should process each event; use a topic when several independent consumers need a copy.
4. Choose a stable partition or ordering key, such as order ID or customer ID, so related events keep their sequence.
5. Assume at-least-once delivery. Give every event an ID and record processed IDs in the same transaction as the business side effect.
6. Retries need exponential backoff with jitter; after the attempt limit, move the message to a dead-letter queue with the original payload and error context.
7. A poison message must not block an entire partition forever. Alert on DLQ depth and provide a safe replay path.
8. Validate event schema and version at ingress; reject unknown critical fields rather than letting consumers guess.
9. If you promise strict order, limit parallelism per key; scaling beyond the number of ordered partitions does not help that key.
10. In the emulator, publish the same event twice and force repeated failures. Use `terraform plan` to check queue/topic settings, redrive policy, retention, and permissions.

## Note

A hint is not an answer: name the deduplication store and the ordering key before writing the consumer flow.

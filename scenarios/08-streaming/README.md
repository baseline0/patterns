# README: Clickstream streaming pipeline

## Learning objective

Design a clickstream pipeline that handles ingestion, partitioning, event-time windowing, backpressure, replay, and schema evolution without running a live stream.

## Scenario story

A product team wants near-real-time click counts and fraud signals from web and mobile clients. Events arrive out of order, a popular campaign creates a hot user key, and analysts ask to replay last week after a bug in an aggregation. The design must tolerate all three without losing the original events.

## Constraints

- Use generic streaming terms. If you name provider services, name all three: AWS, Azure, and GCP.
- No live ingestion, real user data, or cloud streaming jobs.
- Local emulator and `terraform plan` only; synthetic events are allowed locally.
- Preserve raw events so results can be recomputed.
- Work within a 30-60 minute drill.

## Success criteria

- Durable append-only ingestion with a stated partition key and ordering scope.
- Event-time windows with a watermark and allowed lateness rule.
- Backpressure controls with consumer-lag signals and scaling or shedding behavior.
- Raw retention and a replay procedure that avoids duplicate sink writes.
- A schema-versioning rule that distinguishes additive and breaking changes.
- Validation uses synthetic local events, replay checks, and `terraform plan` only.

## Plan-only / cost-free boundary

Write topic, partition, window, and schema notes locally. Publish synthetic events to the local emulator if supported. Use `terraform plan` to review topic retention, partitions where configurable, schema settings, and consumer permissions. Do not create cloud streams, connect real clients, or run managed analytics jobs.

## Starter structure

```
scenarios/08-streaming/
  README.md
  HINTS.md
  SOLUTION.md
  RUBRIC.md
  plan/
    topics.md
    windows.md
    schema.md
  schemas/
  terraform/
```

Sketch these paths in notes; only the four committed documents are required for the drill.

## Exercise (30-60 minutes)

- 0-10 min: Define the event shape and choose a partition key; explain the ordering guarantee.
- 10-25 min: Choose tumbling or session windows and set event-time lateness rules.
- 25-35 min: Add backpressure signals and a hot-key mitigation.
- 35-45 min: Design raw retention and a replay path with idempotent sink writes.
- 45-55 min: Define compatible and breaking schema changes.
- 55-60 min: List synthetic/plan evidence and self-score with the rubric.

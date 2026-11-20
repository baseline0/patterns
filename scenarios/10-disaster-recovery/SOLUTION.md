# SOLUTION: Regional disaster recovery

## Model solution

Set RTO and RPO from business impact. Compare backup/restore, pilot light, and warm standby against those targets and choose the least expensive option that meets them. Keep both regions defined in shared infrastructure code. Use continuous backup plus replication, a monitored replica in the secondary region, and a runbook that names the failover owner, trigger, traffic-routing change, and failback steps. Validate with a local restore, `terraform plan`, and a tabletop failover test.

Provider mapping, using generic names elsewhere: AWS uses cross-region replicas, object storage backups, and DNS failover; Azure uses geo-replication, blob backups, and Traffic Manager; GCP uses cross-region read replicas, Cloud Storage, and global load balancing.

## Rationale

- RTO/RPO convert business impact into measurable design constraints.
- Continuous backup and point-in-time restore handle accidental deletion or corruption; replication handles regional loss.
- Pilot light lowers cost while preserving a restore path; warm standby lowers failover time at higher cost.
- Shared modules with per-region variables reduce configuration drift.
- A named owner and trigger prevent hesitation during an incident.
- Replication-lag monitoring prevents promotion that would violate RPO.
- Single-writer failback prevents split-brain and duplicate transactions.

## Architecture

```
Primary region
  app tier -> database -> continuous backup vault
                    |
                    `-> replication -> Secondary region replica

Secondary region
  IaC skeleton + secret references + optional scaled app tier (warm standby)
                    |
                    v
Failover: trigger -> owner declares -> verify lag -> promote replica
                  -> update traffic routing -> verify reads/writes -> communicate

Failback: drain secondary -> resynchronize to primary -> stop writes -> switch back
```

## Trade-offs

- Backup/restore is low cost but RTO depends on restore time and data replay.
- Pilot light needs scaling during failover, adding time and operational risk.
- Warm standby costs more but shortens detection-to-service time.
- Active-active removes a single control point but makes consistency and conflict handling much harder.
- Near-zero RPO replication is expensive and can amplify latency into normal writes.
- Short DNS TTLs improve failover speed but add resolver load and cost.

## Failure modes

- Backups exist but restore was never tested or omits config and secret references.
- Replication lag exceeds RPO and promotion loses too much data.
- Secondary region IaC has drifted from primary.
- Failover owner unavailable and no deputy named.
- Cached routing keeps users pointed at the failed region.
- Both regions accept writes during failover or failback, causing split-brain.
- Failover script assumes a resource name that exists only in primary.
- Runbook has no communication steps, so users and support learn late.

## Local validation only

- Use the emulator to list modeled backup settings, retention, replica configuration, and routing health checks.
- Perform an isolated local restore into a separate namespace and verify the restored data and config references.
- Run `terraform plan` for the secondary region using shared modules and secondary variables; confirm no unintended primary changes.
- Record replication lag from a local metric stub and apply the promotion rule in notes.
- Run a tabletop failover and failback with timestamps, named decision owner, and communication steps.
- Do not promote a real replica, change DNS, copy production secrets, or contact a real provider.

## Note

A failover test is a schedule, not a wish. Name the date, owner, scope, and abort criteria before the incident.

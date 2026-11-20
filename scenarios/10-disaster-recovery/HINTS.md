# HINTS: Regional disaster recovery

## Progressive hints

1. Start with business impact: how long can the service be down, and how much data loss is acceptable.
2. RPO drives backup frequency or replication mode; RTO drives how warm the standby must be.
3. Backup/restore is cheapest but usually slowest; warm standby is fastest but most expensive; pilot light sits between them.
4. A backup is only useful if restore is tested, including data, config, secret references, and infrastructure definitions.
5. Keep both regions defined in infrastructure code with shared modules and different variables to avoid drift.
6. A pilot light keeps the database replica and minimal control plane ready, then scales compute during failover.
7. Warm standby keeps scaled compute and a warm database ready; verify it is not silently receiving user writes.
8. Failover needs a named decision owner, a trigger condition, and a communication path before the incident.
9. Traffic routing needs health checks and short TTLs; cached routing can delay a failover even after promotion.
10. Monitor replication lag and refuse promotion if lag exceeds the RPO budget.
11. Failback must drain traffic, resynchronize, and enforce a single writer to avoid split-brain.
12. Validate with local restore, emulator inspection, `terraform plan` for the secondary region, and a tabletop walkthrough.

## Note

A strategy that cannot meet the stated RTO/RPO is not a candidate. Change the strategy or renegotiate the objective explicitly.

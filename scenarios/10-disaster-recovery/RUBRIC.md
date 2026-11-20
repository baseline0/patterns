# RUBRIC: Regional disaster recovery

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| RTO/RPO alignment | 4 | RTO and RPO are stated, justified by impact, and used to select the strategy. | Technology chosen first with no stated recovery targets. |
| Backup and restore design | 4 | Continuous backups, restore scope, retention, config, secret references, and IaC are covered; restore is testable. | Backups exist but restore scope or test is undefined. |
| Strategy choice | 4 | Backup/restore, pilot light, and warm standby are compared; chosen option fits RTO/RPO and cost. | Strategy cannot meet targets or comparison is missing. |
| Failover and failback runbook | 4 | Trigger, owner, lag check, routing change, communication, single-writer failback, and deputies are explicit. | No owner, no trigger, or split-brain risk unaddressed. |
| Plan-only validation | 4 | Local restore, emulator inspection, secondary-region `terraform plan`, and tabletop test; no live failover. | Validation requires real promotion or DNS change. |

Total: 20 points.

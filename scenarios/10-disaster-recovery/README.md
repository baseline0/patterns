# README: Regional disaster recovery

## Learning objective

Design regional disaster recovery from business RTO and RPO targets, choose between backup/restore, pilot light, and warm standby, and define a tested failover and failback procedure.

## Scenario story

A primary region loses availability for several hours. The service runs in one region today, backups exist but have never been restored, and no one knows who may declare a failover. Leadership needs RTO and RPO numbers, a recovery option that fits the budget, and a failover test plan that can be rehearsed without touching production.

## Constraints

- Use generic DR terms. If you name provider services, name all three: AWS, Azure, and GCP.
- No live failover, live promotion, DNS change, or data replication to a real region.
- Local emulator and `terraform plan` only; tabletop exercises and local restore drills are allowed.
- Derive the strategy from RTO/RPO, not from a preferred technology.
- Work within a 30-60 minute drill.

## Success criteria

- RTO and RPO are stated with a business justification.
- Backup/restore, pilot light, and warm standby are compared against those targets.
- Backups cover data, configuration, secrets references, and infrastructure definitions.
- Failover trigger, decision owner, traffic-routing change, and communication path are explicit.
- Failback avoids split-brain and duplicate writes.
- Validation uses local restore, emulator inspection, `terraform plan`, and a tabletop test only.

## Plan-only / cost-free boundary

Write DR notes, runbooks, and local Terraform for a secondary region definition. Use the emulator to list modeled backup or replica settings and to perform an isolated local restore if supported. Use `terraform plan` for the secondary region. Do not promote a real replica, change DNS, or copy production secrets.

## Starter structure

```
scenarios/10-disaster-recovery/
  README.md
  HINTS.md
  SOLUTION.md
  RUBRIC.md
  plan/
    objectives.md
    strategy.md
    runbook.md
  terraform/
    modules/
    envs/
      primary/
      secondary/
```

Sketch these paths in notes; only the four committed documents are required for the drill.

## Exercise (30-60 minutes)

- 0-10 min: Set RTO/RPO and justify them from business impact.
- 10-25 min: Compare backup/restore, pilot light, and warm standby; choose one.
- 25-40 min: Define backup scope, replication, and traffic-routing failover.
- 40-50 min: Write failover and failback runbooks with owners and timings.
- 50-60 min: Run a tabletop review and list emulator/plan evidence; self-score with the rubric.

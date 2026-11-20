# RUBRIC: Three-tier web application

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| Tier and subnet isolation | 4 | Public edge, private app, isolated data subnets; no public IP on app, cache, or DB; SG references are narrow. | Tiers share a flat network or the DB is internet reachable. |
| Load balancing and health | 4 | LB spans two zones; health checks remove unhealthy targets; replacement capacity is defined. | Single-zone LB or no meaningful health check/failover path. |
| Stateless app and sessions | 4 | App tier is replaceable; sessions are externalized or signed client-side with rotation. | Sticky sessions or local files are the only session mechanism. |
| Cache and data tier | 4 | Cache placement, TTL, invalidation, and DB standby/replica are explicit. | No cache story, stale reads unresolved, or single-zone database only. |
| Emulator and plan-only validation | 4 | Emulator checks routes/SGs/targets; `terraform plan` checks topology and counts; no live resources. | Validation requires live failover or omits network isolation checks. |

Total: 20 points.

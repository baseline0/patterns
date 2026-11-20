# RUBRIC: Serverless URL shortener

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| API shape and routing | 4 | Create and resolve paths are separate; resolve returns a redirect; unknown codes return a stable 404. | Single ambiguous route, HTML response for resolve, or missing not-found behavior. |
| Idempotent create | 4 | Client key or canonical input plus conditional write returns one code under retry and collision. | Retry creates a second record or code generation can overwrite an existing entry. |
| Durable data model | 4 | Codes are keyed for direct lookup; mapping is stored outside function memory; TTL/expiry rule is stated. | Mappings live in memory or require a full scan for lookup. |
| Hot-key strategy | 4 | Cache TTL, single-flight or equivalent, and invalidation on update are defined. | No hot-key handling or cache that can never be refreshed. |
| Validation, security, and plan-only evidence | 4 | URL scheme/host validation, gateway throttling, structured logs, emulator replay test, and `terraform plan` checks are present. | No validation or throttles, secrets in logs, or validation requires live deployment. |

Total: 20 points.

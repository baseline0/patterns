# Architecture catalogue

> Generated from `architecture/content/catalogue.yaml`. Edit YAML, then run `tools/build.py`.

This is the canonical index for design patterns, architecture styles, tactics, quality attributes, and scenarios.

## Families

### Styles (6)

- `cqrs` — Command Query Responsibility Segregation
- `event-driven` — Event-Driven Architecture
- `layered` — Layered Architecture
- `microservices` — Microservices Architecture
- `pipe-and-filter` — Pipe and Filter
- `serverless` — Serverless Architecture

### Tactics (9)

- `blue-green-deploy` — Blue-Green Deploy
- `bulkhead` — Bulkhead
- `cache-aside` — Cache Aside
- `circuit-breaker` — Circuit Breaker
- `idempotent-consumer` — Idempotent Consumer
- `observability` — Observability
- `queue-based-load-leveling` — Queue-Based Load Leveling
- `retry-with-backoff` — Retry with Backoff
- `saga` — Saga

### Quality Attributes (6)

- `availability` — Availability
- `modifiability` — Modifiability
- `performance` — Performance
- `recoverability` — Recoverability
- `security` — Security
- `testability` — Testability

## Scenarios

| ID | Title | Status | Prompt | Solution | Rubric |
| --- | --- | --- | --- | --- | --- |
| `01-static-website` | Static website with CDN | implemented | [README](../scenarios/01-static-website/README.md) | [SOLUTION](../scenarios/01-static-website/SOLUTION.md) | [RUBRIC](../scenarios/01-static-website/RUBRIC.md) |
| `02-serverless-api` | Serverless URL shortener | implemented | [README](../scenarios/02-serverless-api/README.md) | [SOLUTION](../scenarios/02-serverless-api/SOLUTION.md) | [RUBRIC](../scenarios/02-serverless-api/RUBRIC.md) |
| `03-event-driven` | Event-driven order ingress | implemented | [README](../scenarios/03-event-driven/README.md) | [SOLUTION](../scenarios/03-event-driven/SOLUTION.md) | [RUBRIC](../scenarios/03-event-driven/RUBRIC.md) |
| `04-crud-api` | Serverless CRUD API | implemented | [README](../scenarios/04-crud-api/README.md) | [SOLUTION](../scenarios/04-crud-api/SOLUTION.md) | [RUBRIC](../scenarios/04-crud-api/RUBRIC.md) |
| `05-3tier-web` | Three-tier web application | implemented | [README](../scenarios/05-3tier-web/README.md) | [SOLUTION](../scenarios/05-3tier-web/SOLUTION.md) | [RUBRIC](../scenarios/05-3tier-web/RUBRIC.md) |
| `06-cicd-pipeline` | Safe multi-environment CI/CD pipeline | implemented | [README](../scenarios/06-cicd-pipeline/README.md) | [SOLUTION](../scenarios/06-cicd-pipeline/SOLUTION.md) | [RUBRIC](../scenarios/06-cicd-pipeline/RUBRIC.md) |
| `07-monitoring` | Observability and incident response | implemented | [README](../scenarios/07-monitoring/README.md) | [SOLUTION](../scenarios/07-monitoring/SOLUTION.md) | [RUBRIC](../scenarios/07-monitoring/RUBRIC.md) |
| `08-streaming` | Clickstream streaming pipeline | implemented | [README](../scenarios/08-streaming/README.md) | [SOLUTION](../scenarios/08-streaming/SOLUTION.md) | [RUBRIC](../scenarios/08-streaming/RUBRIC.md) |
| `09-microservices` | Microservices order system | implemented | [README](../scenarios/09-microservices/README.md) | [SOLUTION](../scenarios/09-microservices/SOLUTION.md) | [RUBRIC](../scenarios/09-microservices/RUBRIC.md) |
| `10-disaster-recovery` | Regional disaster recovery | implemented | [README](../scenarios/10-disaster-recovery/README.md) | [SOLUTION](../scenarios/10-disaster-recovery/SOLUTION.md) | [RUBRIC](../scenarios/10-disaster-recovery/RUBRIC.md) |

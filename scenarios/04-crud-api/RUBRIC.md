# RUBRIC: Serverless CRUD API

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| Layered design and repository | 4 | Handler, service, repository, and store adapter are distinct; services use domain objects. | SDK calls are spread through handlers or business logic. |
| Validation and error mapping | 4 | Boundary schema plus 400/404/409/500 mapping with no internal detail leakage. | Validation is late or provider exceptions become client responses. |
| Unit of work and optimistic concurrency | 4 | Main write and related writes share a commit boundary; version check returns 409 on conflict. | Blind last-write-wins update or claimed transaction the store cannot provide. |
| Data modeling | 4 | Key and optional index are justified by named access patterns; no scan-dependent list path. | Key chosen arbitrarily or every query requires a full scan. |
| Emulator and plan-only validation | 4 | CRUD sequence, invalid input, missing item, and concurrent conflict tested locally; `terraform plan` checked; no live deploy. | Validation relies on a live cloud database or omits conflict testing. |

Total: 20 points.

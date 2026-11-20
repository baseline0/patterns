# SOLUTION: Serverless URL shortener

## Model solution

Use an API gateway in front of a stateless function. The create endpoint validates input, derives an idempotency key from a client header or canonical long URL, and performs a conditional write into a durable table keyed by short code. The resolve endpoint looks up the code, prefers an edge or in-process cache for hot keys, and returns a redirect. Structured logs and throttles cover both paths.

Provider mapping, using generic names elsewhere: AWS uses API Gateway, Lambda, and DynamoDB; Azure uses API Management, Azure Functions, and Cosmos DB or Table storage; GCP uses API Gateway, Cloud Functions, and Firestore or Bigtable.

## Rationale

- Gateway routing keeps validation, throttling, and CORS out of business logic.
- Conditional writes on the code key make create idempotent under retries.
- A durable store survives function restarts and scale events.
- A small cache with single-flight absorbs hot-key traffic without making stale data permanent.
- A 302 redirect preserves the ability to change or retire a destination.
- Rate limits and URL validation reduce abuse of a public redirector.

## Architecture

```
Create path
Client -> API gateway -> create function -> validate + idempotency key
                                      -> conditional write -> durable table

Resolve path
Client -> CDN/edge cache -> API gateway -> resolve function -> cache lookup
                                                  |-> hit: redirect
                                                  `-> miss: table read -> redirect

Cross-cutting
gateway throttles + structured logs + metrics for create collisions, cache hit rate, and 404s
```

## Trade-offs

- Random codes reduce guessing but need collision handling; sequential codes are compact but enumerable.
- 302 redirects keep flexibility at the cost of more origin reads; 301 reduces reads but makes destination changes painful.
- Edge caching improves hot-key latency but delays target changes until TTL expiry or purge.
- In-process caches are cheap but per-instance and inconsistent; a shared cache adds a dependency.
- Deterministic codes make retries naturally idempotent but can leak information about input.

## Failure modes

- Duplicate creates on client retry without an idempotency key.
- Hot key overwhelms the table or function concurrency during a traffic spike.
- Cache serves an old destination after an update.
- Open redirect or scheme abuse from unvalidated long URLs.
- Throttling too loose allows abuse; too strict breaks legitimate bursts.
- Cold starts add latency to cache misses.
- Collision handling overwrites an existing code if the conditional write is omitted.

## Local validation only

- Use the emulator to create the same link twice with the same idempotency key and confirm one stored record.
- Resolve an unknown code and confirm a 404 with a stable error shape.
- Burst one short code and confirm cache hits or recorded lookup counts before the store is touched again.
- Validate long URLs with disallowed schemes and confirm rejection.
- Run `terraform plan` and verify gateway routes, throttles, table key schema, conditional-write assumptions in code review, and least-privilege roles.
- Do not publish a public endpoint, register a domain, or apply to a real provider.

## Note

Idempotency is proved by the create path, not by the redirect path. A resolve retry is naturally safe; a create retry is not unless the key and conditional write are present.

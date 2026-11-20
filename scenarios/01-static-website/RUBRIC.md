# RUBRIC: Static website with CDN

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| Delivery path and origin isolation | 4 | CDN is the public entry point; object store is private; only the CDN identity can read origin objects. | Origin is publicly readable or clients can bypass the CDN path. |
| Cache and invalidation strategy | 4 | Hashed assets use long TTL; HTML uses short TTL or no-cache; release/invalidation path is explicit. | All objects share one TTL or no invalidation/release story is described. |
| HTTPS and access controls | 4 | TLS terminates at the edge; HTTP redirects to HTTPS; WAF/rate limits and least-privilege origin access are defined. | Plain HTTP allowed, origin policy broad, or WAF/rate limits absent. |
| CORS and observability | 4 | CORS allowlist is minimal and explicit; access logs include request IDs for allowed and blocked requests. | CORS is wildcard or undefined; no logging or request correlation described. |
| Emulator and plan-only validation | 4 | Emulator checks object metadata, headers, and access; `terraform plan` checks CDN, TLS, WAF, and policy; no live deployment. | Validation depends on deploying to a real cloud or omits plan/emulator evidence. |

Total: 20 points.

# HINTS: Serverless URL shortener

## Progressive hints

1. Split the design into two paths: create a short link and resolve a short code.
2. A create request should accept a long URL and an optional client idempotency key; a resolve request should return a redirect, not a rendered page.
3. Generate short codes from a random base62 value or a compact hash plus collision check. Avoid exposing raw sequential counters if links may be guessed.
4. Make create safe to retry: with the same key or same canonical input, return the same short code instead of writing a second row.
5. Use a conditional write on the short-code key so two simultaneous creates cannot produce different codes for the same input.
6. Keep mappings in a durable key-value/table store. Function memory is useful only as a short-lived cache, never as the source of truth.
7. For a hot code, add an edge or in-process cache with a small TTL and single-flight behavior so a burst does not stampede the store.
8. Decide redirect semantics deliberately: a 302 keeps destination changes easy, while a 301 allows longer caching but makes changes harder.
9. Validate scheme and host to prevent open redirects or abuse, and apply throttling at the gateway.
10. In the emulator, replay the same create twice and burst one popular code. Use `terraform plan` to check routes, store keys, throttles, and least-privilege roles.

## Note

These are hints, not a completed design. Stop before choosing exact TTLs or status codes if you have not yet justified them.

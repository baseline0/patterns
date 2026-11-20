# SOLUTION: Static website with CDN

## Model solution

Publish each release as immutable objects in a private object store. A CDN sits in front of that origin and terminates TLS. The CDN cache serves hashed assets for a long TTL and the HTML entry document for a short TTL. A new release writes a new version prefix, then updates the entry document; invalidation is limited to that document.

Provider mapping, using generic names elsewhere: AWS uses object storage, CDN, WAF, and a managed certificate service; Azure uses Blob Storage, Front Door, WAF, and managed certificates; GCP uses Cloud Storage, Cloud CDN, Cloud Armor, and managed TLS.

## Rationale

- A private origin prevents clients from bypassing the CDN, WAF, and TLS policy.
- Hashed asset filenames make cache invalidation unnecessary for CSS, JavaScript, and images.
- A short-lived entry document limits stale HTML after a release while keeping static assets cacheable.
- TLS at the edge gives users HTTPS without adding compute.
- WAF and rate limits reduce volumetric and common web attacks before they reach storage.
- A narrow CORS policy allows required browser behavior without opening the origin to arbitrary sites.

## Architecture

```
Author / build job
        |
        v
Release artifacts (hashed assets)
        |
        v
Private object store (origin)
        ^
        | restricted origin read
        |
Client -> DNS -> CDN edge (TLS + WAF + rate limit)
                   |-> cache: hashed assets, long TTL
                   |-> cache: index.html, short TTL
                   |-> CORS and security headers
                   `-> access logs with request ID
```

## Trade-offs

- CDN plus WAF adds configuration and cost, but removes origin exposure and reduces latency.
- Versioned prefixes avoid purges but leave old objects until a lifecycle rule removes them.
- Short HTML TTL reduces staleness but increases origin reads for the entry document.
- Strict origin access improves security but makes direct debugging harder; use a separate break-glass role instead of a public bucket.
- Broad CORS is easy but weakens browser isolation; keep the allowlist explicit.

## Failure modes

- Stale HTML points to an old asset version after a release.
- Cache purge misses a path or triggers a stampede on the origin.
- Origin is accidentally public, bypassing WAF and TLS enforcement.
- Incorrect content type causes browsers to download CSS or JavaScript.
- CORS omits a font or API origin, breaking the page in the browser only.
- WAF false positives block legitimate requests; request IDs are needed to diagnose.
- Certificate or redirect misconfiguration creates an HTTP-to-HTTPS loop.

## Local validation only

- Start the local emulator and confirm objects, content types, and hashed filenames in the release prefix.
- Check that anonymous reads are denied and that only the CDN-origin identity has read access.
- Request objects through the emulator and inspect CORS and security headers.
- Run `terraform plan` and verify the distribution origin, TLS policy, cache policies, WAF link, and bucket policy.
- Record which behaviors the emulator cannot prove, especially edge caching and global propagation.
- Do not create DNS records, certificates, WAF policies, or cloud resources; do not run apply against a real provider.

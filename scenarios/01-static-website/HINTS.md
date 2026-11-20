# HINTS: Static website with CDN

## Progressive hints

1. Treat the object store as a private origin, not as the public front door. The CDN should be the only identity allowed to read objects.
2. Separate mutable and immutable content. Give CSS, JavaScript, and images content hashes in their filenames so they can be cached for a long time.
3. Keep the HTML entry document on a short TTL or no-cache policy. A release should change the HTML pointer rather than overwrite hashed assets in place.
4. Prefer versioned release prefixes over emergency purges. If a purge is needed, purge only the entry document and a small set of known paths.
5. Terminate TLS at the edge. Redirect HTTP to HTTPS, use a managed certificate, and enable HSTS only after the redirect path is proven.
6. Add the minimum CORS policy needed for fonts, scripts, or cross-origin API calls. Allow only the origins, methods, and headers actually used.
7. Put managed WAF rules and rate limits at the edge, and log both allowed and blocked requests with request IDs.
8. In an emulator, focus on object metadata, content types, CORS headers, and access policy. Edge cache behavior and WAF inspection are usually only partially modeled.
9. Use `terraform plan` to confirm distribution origin, TLS policy, cache policies, WAF association, and bucket policy. Do not rely on the emulator to prove global propagation.

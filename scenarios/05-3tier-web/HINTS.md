# HINTS: Three-tier web application

## Progressive hints

1. Draw three trust zones before choosing any service: internet-facing edge, private app capacity, and isolated data tier.
2. Only the load balancer should have a public route. App instances and the database should have no public IPs.
3. Put load balancer targets in at least two failure zones; health checks should remove a bad instance from rotation.
4. Keep app instances replaceable. If a restart loses the user's session, the tier is not stateless.
5. Move sessions to a shared session store or signed client-side state with rotation; avoid sticky sessions as the only answer.
6. Use a cache for hot reads. Define cache-aside behavior, a TTL, and what happens to the cache entry after a write.
7. Chain security groups by reference where possible: edge group allows app port, app group allows DB port, DB group accepts only from app.
8. Give the database no default route to the internet. Use private endpoints or NAT only for the app tier's outbound needs.
9. Add a standby or replica in a second zone and state how a zone failure is detected.
10. The emulator can show subnets, routes, and groups but not real failover. Use `terraform plan` to verify references and counts.

## Note

Do not solve availability by adding more app instances if the database or session store is still a single point of failure.

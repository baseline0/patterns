# SOLUTION: Three-tier web application

## Model solution

Place an internet-facing load balancer in public subnets across two failure zones. Route only to stateless app instances in private subnets, with health checks on a dedicated endpoint. Store sessions in a shared store or signed client-side state. Put a read cache in front of an isolated database with a standby or replica in a second zone. Security groups reference each other instead of broad CIDRs.

Provider mapping, using generic names elsewhere: AWS uses VPC, Application Load Balancer, EC2 Auto Scaling, RDS, and a managed cache; Azure uses VNet, Application Gateway, VM Scale Sets, Azure SQL, and a managed Redis cache; GCP uses VPC, Cloud Load Balancing, Managed Instance Groups, Cloud SQL, and Memorystore.

## Rationale

- Subnet isolation limits the blast radius of a compromised edge or app instance.
- A load balancer with health checks hides instance failure from users.
- Stateless app instances can be replaced or scaled without losing user sessions.
- A shared session store makes capacity changes safe.
- Cache-aside reduces repeated read load while writes invalidate or expire the entry.
- A database standby or replica in another zone covers zone loss.
- Security-group chaining prevents accidental wide-open database access.

## Architecture

```
Internet
   |
   v
Internet gateway -> Load balancer (public subnets, TLS termination)
   | health checks
   v
App tier (private subnets, auto-scaled, stateless)
   |            \
   |             -> shared session store
   v
Read cache (private)
   |
   v
Database (isolated data subnets, standby/replica in second zone)

Security: edge SG -> app SG -> DB SG; no public IP on app, cache, or DB
```

## Trade-offs

- Managed databases and caches cost more but remove patching and failover work.
- Caching improves read latency but adds invalidation and staleness concerns.
- A shared session store adds a dependency but enables true stateless app tiers.
- Sticky sessions are simpler but slow scale-out and fail when an instance disappears.
- Multi-zone database replicas improve availability but increase cost and replication complexity.
- NAT or private endpoints enable outbound access but add cost or configuration.

## Failure modes

- Database placed in a public subnet or given a default internet route.
- Sticky sessions masking local state, causing session loss on instance replacement.
- Cache stampede after a mass expiry or purge.
- Stale cached reads after a write because invalidation was omitted.
- Security group allows the whole CIDR instead of the calling group.
- Health check points at a shallow endpoint that does not test dependencies.
- Connection pool exhaustion when app instances scale faster than the database can accept.
- Zone failure leaves the app scaled but the database without a promoted standby.

## Local validation only

- Use the emulator to inspect subnets, route tables, security groups, and load balancer target groups.
- Confirm no public IP is attached to app, cache, or database resources.
- Send a local request to the modeled load balancer endpoint if the emulator supports it, and check the health response shape.
- Simulate an unhealthy target locally and confirm the target group removes it from rotation.
- Run `terraform plan` and verify resource counts across two zones, SG references, database isolation, and cache placement.
- Note that real zone failover and managed database promotion cannot be proved locally.
- Do not create live instances, databases, load balancers, or public addresses.

## Note

Availability is a chain. The database and session store must be as available as the app tier for the design to meet its promise.

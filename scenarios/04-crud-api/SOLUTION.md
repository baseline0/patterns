# SOLUTION: Serverless CRUD API

## Model solution

Use a thin HTTP handler over an application service. The service owns validation, use cases, and a unit of work. A repository interface separates domain objects from the provider store. Each item carries a version; updates use a conditional write on that version, producing a 409 conflict when another writer won. Responses are mapped to stable HTTP statuses.

Provider mapping, using generic names elsewhere: AWS uses API Gateway, Lambda, and DynamoDB; Azure uses API Management or HTTP Functions, Azure Functions, and Cosmos DB; GCP uses API Gateway, Cloud Functions, and Firestore or Spanner.

## Rationale

- Layering keeps transport concerns out of business rules and makes the handler easy to test.
- A repository allows an emulator adapter or test double without changing the service.
- A unit of work keeps the main write and related audit/outbox writes consistent.
- Optimistic concurrency prevents lost updates without holding long database locks.
- Boundary validation gives clients predictable 400 responses instead of provider exceptions.
- Domain objects returned from the repository avoid leaking SDK types across layers.

## Architecture

```
HTTP request
   |
   v
API gateway / router
   |
   v
Handler: parse, authenticate, validate, map status
   |
   v
Application service: use case + unit of work
   |
   v
Repository interface
   |
   v
Store adapter -> durable table (key + version + conditional write)
   |
   v
Response mapper: 200 / 201 / 400 / 404 / 409 / 500
```

## Trade-offs

- Key-value stores scale well for direct lookups but make ad hoc joins expensive.
- Optimistic concurrency avoids locks but pushes conflict handling to clients.
- A repository adds indirection but keeps provider details out of tests and services.
- Strict validation catches bad input early but can reject clients that relied on loose fields.
- Transactional units of work are safer but may cost more and be unavailable across some store boundaries.

## Failure modes

- Lost update when an update writes without checking the expected version.
- Repository returns raw provider items, coupling services to the SDK.
- Validation occurs after the store call, causing unnecessary writes and inconsistent errors.
- Provider exception text leaks into 500 responses.
- Hot partition when all items share a low-cardinality key.
- Eventual consistency makes a read-after-write appear missing if the wrong consistency mode is used.
- Partial writes when the unit of work cannot actually commit atomically.

## Local validation only

- Use the emulator to run create, list, get, update, and delete in sequence.
- Submit an invalid body and confirm a 400 with field-level detail.
- Request a missing ID and confirm a 404.
- Submit two updates with the same expected version and confirm one 200 and one 409.
- Confirm the repository adapter is the only layer importing provider SDK types.
- Run `terraform plan` and verify gateway routes, table key schema, version attribute usage in code review, audit/outbox design, and least-privilege roles.
- Do not call a real cloud API or provision a managed database.

## Note

If the store lacks multi-item transactions, keep the audit record in the same item or explicitly accept the consistency gap. Do not claim a unit of work that the adapter cannot enforce.

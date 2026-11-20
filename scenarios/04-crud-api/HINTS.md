# HINTS: Serverless CRUD API

## Progressive hints

1. Draw four layers: transport, application service, repository, and store. The HTTP handler should only parse, validate, call a use case, and map the response.
2. Define the repository interface in domain terms, such as `get_todo` or `save_todo`, not in provider SDK terms.
3. A unit of work should cover the main write and any audit or outbox write so they succeed or fail together.
4. Validate at the boundary with an explicit schema. Reject wrong types and unknown critical fields with a 400 and field-level detail.
5. Add a version attribute to each item. Updates should include the expected version in a conditional write and return 409 when it no longer matches.
6. Map storage outcomes deliberately: missing item to 404, conflict to 409, validation failure to 400, and unexpected failure to 500 without leaking internals.
7. Choose the primary key from the actual access pattern. Avoid a design where listing requires scanning the whole table.
8. Add a secondary index only for a named query pattern; each index adds cost and consistency considerations.
9. Return domain objects from the repository, not raw SDK responses, so the rest of the code stays provider-neutral.
10. In the emulator, run the full create-read-update-delete sequence and two concurrent updates with the same version. Use `terraform plan` to check routes, table keys, and least-privilege roles.

## Note

The optimistic-concurrency check is the core trade-off in this drill. Do not replace it with a blind last-write-wins update.

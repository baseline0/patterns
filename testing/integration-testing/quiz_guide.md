# Quiz: Integration testing: service boundaries, fixture lifecycle, and database tests

> Generated from `content/`.

## 1. What is the main difference between unit tests and integration tests?

A. Unit tests are faster and test components in isolation; integration tests verify interactions between components
B. Integration tests are always faster because they use mocking
C. Unit tests require mocking; integration tests never use mocks
D. Integration tests always use a real database

**Answer: A.** Unit tests isolate components; integration tests verify cross-component interactions. Integration tests may use real databases or in-memory replicas.

## 2. What does a session-scoped fixture do?

A. Runs setup before each test
B. Runs setup once per test session and reuses it across all tests
C. Runs setup once per test module
D. Disables setup and teardown entirely

**Answer: B.** Session-scoped fixtures run setup once and reuse the result across all tests in the session. This amortizes expensive setup cost but requires careful cleanup.

## 3. How does transaction rollback keep database tests isolated?

A. It reverts all changes after each test, so the database is clean for the next test
B. It prevents tests from writing to the database
C. It duplicates the database for each test
D. It disables database commits entirely

**Answer: A.** A test's writes are wrapped in a transaction that rolls back, leaving the database clean. No explicit cleanup needed; the database is fresh for the next test.

## 4. What is a contract test?

A. A test that verifies a service conforms to its API contract (request/response format)
B. A test that always passes
C. A test that uses mocking instead of real services
D. A test that runs only on Sundays

**Answer: A.** Contract tests verify that both client and server agree on API format (schema, status codes, error messages). Misalignment breaks the contract.

## 5. Why might you use a module-scoped fixture instead of a session-scoped one?

A. Module scope runs faster because it reuses setup across more tests
B. Module scope provides finer isolation granularity; setup is shared per module, not per session
C. Module scope is always slower and should be avoided
D. Module scope disables cleanup

**Answer: B.** Module scope balances speed (reuse setup per module) and isolation (fresh setup for each new module). It's a middle ground between function and session scopes.

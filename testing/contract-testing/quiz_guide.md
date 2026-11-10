# Quiz: Contract testing: API contracts and consumer-driven contracts

> Generated from `content/`.

## 1. What is a consumer-driven contract?

A. A contract where the server defines all the rules and the client must obey
B. A contract where the client defines expectations and the server implements to meet them
C. A contract that is agreed upon after integration issues occur
D. A contract that only applies to external APIs

**Answer: B.** Consumer-driven contracts empower clients to define their needs; providers implement to satisfy the contract.

## 2. How do contract tests differ from end-to-end tests?

A. Contract tests are slower because they test the entire system
B. Contract tests are faster because they focus on API format, not full system behavior
C. Contract tests require a running server; end-to-end tests do not
D. Contract tests and end-to-end tests are the same thing

**Answer: B.** Contract tests validate API format without requiring full service startup. They're faster than end-to-end tests and provide quicker feedback.

## 3. What does jsonschema.validate(response, schema) do?

A. It sends a request to verify the server is running
B. It checks that the response matches the expected schema (required fields, types)
C. It converts the response to a different format
D. It compresses the response for storage

**Answer: B.** jsonschema.validate checks that the response conforms to the schema: required fields are present, types are correct, and no extra fields violate constraints.

## 4. Why should contract tests run in CI?

A. To slow down the build and catch fewer bugs
B. To catch breaking changes before merging, preventing integration failures
C. To replace all unit and integration tests
D. To verify that the code is fast enough

**Answer: B.** Contract tests in CI fail when an API change breaks compatibility, preventing merges and catching issues early before they reach production.

## 5. What should happen if a provider contract test fails?

A. Ignore the failure and merge anyway
B. Fix the implementation to satisfy the contract, or update the contract if intentional
C. Always update the contract to match the implementation
D. Delete the contract test

**Answer: B.** A failing provider contract means the implementation doesn't meet the contract. Either fix the implementation or intentionally update the contract (and notify clients).

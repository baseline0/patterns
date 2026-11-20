# Contract testing: API contracts and consumer-driven contracts

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

Contract tests verify that a client and a server agree on the shape and behavior of their API: request format, response schema, status codes, and error handling. Consumer-driven contracts start with the client's expectations and verify the server meets them. Provider contracts test the server's behavior independently. Contract tests prevent integration breaks: when a contract test fails, the API has changed in a way that breaks the client. Contract tests are faster than end-to-end tests and catch misalignment early.

## Consumer-driven contracts: client defines expectations

The client (consumer) defines what it expects from the server (provider) in a contract file. The contract specifies request format, response schema, status codes, and error messages. The provider implements to satisfy the contract; both sides validate against it.

## Provider contracts: server defines its capabilities

The provider defines what it guarantees: API version, supported methods, response schemas. The provider tests that it meets its contract. When a consumer violates the contract (e.g., sends invalid input), the provider's contract test might not catch it, but the consumer's contract test should.

## Schema validation as a lightweight contract test

Without a formal contract framework (like Pact), schema validation can enforce contracts: jsonschema, OpenAPI specs, or GraphQL schemas. Tests validate requests against schemas before sending and responses after receiving. This catches misalignment faster than end-to-end tests.

## Contract tests in CI catch breaking changes early

Contract tests run in CI before merging. If a PR changes the API in a breaking way, the contract test fails, preventing the merge. This is faster feedback than waiting for end-to-end tests or production issues.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `consumer-driven contract test (client expectations)` | O(1) milliseconds | no service calls; validates against schema |
| `provider contract test (server behavior)` | O(n) where n is number of scenarios | server must respond to all expected requests |
| `schema validation (request or response)` | O(n) where n is schema depth | linear in schema complexity |
| `end-to-end test (full client + server interaction)` | O(n) seconds | slower than contract tests; full startup and teardown |
| `contract test in CI with multiple consumers` | O(n*m) where n is consumers, m is scenarios per consumer | parallelizable; each consumer's tests run independently |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| API client and server agree on request/response format before integration | Prevent breaking changes; catch misalignment early | consumer-driven contract (Pact) or schema validation (JSON Schema, OpenAPI) | `jsonschema for schema validation; Pact for formal contracts` | verify that GET /api/health returns {status: 'ok'} and status 200 |
| Prevent API breaking changes in CI before merging | Fail the contract test if API changes incompatibly | contract test in CI; run against main branch and PR branch | `pytest with contract assertions; Pact broker for distributed contracts` | contract test fails if response schema changes |
| Validate that a request matches the API schema before sending | O(1) per request; fail fast if schema is violated | JSON Schema validation on request construction | `jsonschema.validate(request, request_schema)` | verify request body has required fields and correct types |
| Validate that a response matches the expected schema after receiving | O(1) per response; fail fast if schema is violated | JSON Schema validation on response processing | `jsonschema.validate(response, response_schema)` | verify response has status, data, and optional error fields |
| Test error scenarios: client sends invalid input, server returns correct error | Both sides agree on error format and status codes | contract test with error scenarios | `pytest with error assertions; schema validation on error response` | verify that POST /api/item with missing 'name' returns 400 {error: 'name required'} |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| 1. Define API contract between client and server | Pact file or JSON Schema | consumer-driven contract: client defines expectations, server implements | `Pact CLI or jsonschema` | Formal contracts prevent misalignment; both sides validate against the contract before integrating. |
| 2. Validate API request against schema before sending | request object + JSON Schema | validate request before making HTTP call | `jsonschema.validate(request, schema)` | Catching schema violations early saves time debugging invalid requests. |
| 3. Validate API response against schema after receiving | response object + JSON Schema | validate response after receiving HTTP response | `jsonschema.validate(response, schema)` | Mismatched responses are caught immediately, not silently processed as wrong data. |
| 4. Test that error responses match the contract (error format, status code) | contract test with error scenarios | send invalid request, assert error status and error message format | `pytest with assertions on response status and body` | Clients rely on error format and codes; contracts ensure consistency. |
| 5. Prevent API breaking changes in CI | contract test in CI pipeline | run contract tests for main and PR; fail if contract is violated | `CI integration with pytest` | Catching breaking changes before merge prevents integration failures and reduces incidents. |

## Claims and their checks

- `contract-tests-prevent-api-misalignment`: Contract tests verify that both client and server agree on API format before integration.
- `consumer-driven-contracts-empower-clients`: Consumer-driven contracts let clients define their needs; providers implement to meet them.
- `contract-tests-are-faster-than-e2e-tests`: Contract tests don't require full service startup; they're faster than end-to-end tests and provide quicker feedback.
- `schema-validation-enforces-contracts-without-pact`: JSON Schema, OpenAPI, and GraphQL schemas enforce contracts; tests validate requests and responses.
- `contract-tests-in-ci-prevent-breaking-changes`: Contract tests fail when an API change breaks compatibility, preventing merges and catching issues early.

## Code Examples

### Consumer-driven contract: Pact definition

```python
"""Consumer-driven contract in Pact format."""
{
  "interactions": [
    {
      "description": "a request for health status",
      "request": {
        "method": "GET",
        "path": "/healthz"
      },
      "response": {
        "status": 200,
        "body": {
          "status": "ok"
        }
      }
    }
  ]
}
# The client expects GET /healthz to return {status: "ok"} with status 200.
# The server must satisfy this contract.

```

### Schema validation: validate request

```python
"""Validate request against JSON Schema before sending."""
from jsonschema import validate, ValidationError

request_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["name"]
}

request_data = {"name": "Alice", "age": 30}
validate(instance=request_data, schema=request_schema)
# If request_data were {"age": 30}, validation would fail: 'name' is required.

```

### Schema validation: validate response

```python
"""Validate response against JSON Schema after receiving."""
from jsonschema import validate

response_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "status": {"type": "string", "enum": ["active", "inactive"]}
    },
    "required": ["id", "name", "status"]
}

response = {"id": 1, "name": "Alice", "status": "active"}
validate(instance=response, schema=response_schema)
# If response were {"id": 1, "name": "Alice"}, validation would fail: 'status' is required.

```

### Contract test: error response format

```python
"""Test that error responses match the contract."""
import requests
from jsonschema import validate

error_schema = {
    "type": "object",
    "properties": {
        "error": {"type": "string"},
        "code": {"type": "string"}
    },
    "required": ["error", "code"]
}

def test_error_response_format():
    response = requests.post("http://localhost:8080/api/item", json={})
    assert response.status_code == 400
    validate(instance=response.json(), schema=error_schema)
# The contract specifies error format and status code; the test verifies both.

```

### OpenAPI schema as contract

```python
"""OpenAPI spec as a contract for API clients and servers."""
openapi: 3.0.0
info:
  title: Work Item API
  version: 1.0.0
paths:
  /api/items:
    get:
      responses:
        200:
          description: List of work items
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id: {type: integer}
                    task: {type: string}
                  required: [id, task]
# The OpenAPI spec defines the contract; both client and server must conform.

```

### Contract test CI failure prevents breaking changes

```python
"""Contract test in CI: fails if API changes incompatibly."""
def test_contract_health_endpoint():
    # This test is part of CI
    response = requests.get("http://localhost:8080/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
# If a PR changes the response to {"health": "ok"}, the test fails, blocking the merge.

```

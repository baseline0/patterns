# Integration testing: service boundaries, fixture lifecycle, and database tests

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

Integration tests verify interactions between multiple components: a service calling a repository, a repository querying a database, or an API calling a downstream service. Unlike unit tests, integration tests may use real databases (or in-memory replicas), but they must still be hermetic and reproducible. Fixture scopes (function, session, module) manage expensive setup; transaction rollback keeps tests isolated. Contract tests define boundaries between services and verify both sides adhere to the contract.

## Define service boundaries and test across them

A service (e.g., fleet-ops orchestration) depends on a repository (e.g., work-item store). Integration tests verify the service calls the repository correctly and handles results. These tests may use a real repository (local SQLite) or a mock, depending on the boundary's cost and realism.

## Fixture scope controls setup reuse and isolation

Fixture scope (function, class, module, session) determines how often setup runs and when teardown occurs. A function-scoped fixture runs before each test; a session-scoped fixture runs once per test session. Choose scopes to balance speed (reuse expensive setup) and isolation (avoid test coupling).

## Transaction rollback keeps database tests isolated

Tests that write to a database can roll back transactions after each test, ensuring clean state. SQLAlchemy's session fixture can wrap each test in a transaction that rolls back, so the database is clean for the next test without explicit teardown.

## Contract tests enforce API boundaries

A contract test verifies that both a client and a server adhere to their agreement (API schema, request/response format, error codes). Consumer-driven contracts start with the client's expectations. Provider contracts test the server's behavior. Both must pass; misalignment breaks the contract.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `integration test (real database, transaction rollback)` | O(n) milliseconds to seconds, depends on database operations | may hit real I/O; slower than unit tests |
| `session-scoped fixture (database connection, expensive setup)` | O(1) setup per session; reused across all tests | amortizes expensive setup cost |
| `module-scoped fixture` | O(1) setup per module | finer granularity than session, coarser than function |
| `function-scoped fixture (cleanup after each test)` | O(n) where n is number of tests | most isolation; all setup/teardown happens per-test |
| `contract test (verify request/response schemas)` | O(1) for each contract assertion | fast; no external service calls, just schema validation |
| `parallel integration tests (pytest-xdist with real database)` | O(n/p) but limited by database connection pool | parallelism may be bottlenecked by database access |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Test interaction between a service and a repository or external dependency | Slower than unit tests, but still deterministic and repeatable | real or in-memory database, service layer, integration fixture | `@pytest.fixture(scope='module'), SQLAlchemy session, transaction rollback` | test_work_item_dispatch verifies fleet-ops service calls the work-item repository |
| Test API contract between client and server (request/response format) | Both sides must agree on schema; misalignment is a contract violation | contract test framework (Pact) or manual schema validation | `pytest with custom assertions on request/response shape` | verify that a request to /api/health returns {status: 'ok'} |
| Database tests that need clean state between tests | Each test sees a clean database; no test pollution | transaction rollback fixture or database reset between tests | `@pytest.fixture with connection.rollback() or database reset` | test_insert_work_item; insert, query, verify, rollback |
| Test a workflow across multiple components (end-to-end orchestration) | Slower but realistic; uses real components where possible | integration test with multiple components in-process or containerized | `pytest, docker-compose, or local service instances` | test_workflow_dispatch_and_queue verifies dispatch creates a queued job |
| Reuse expensive setup (database, service startup) across tests | Balance speed and isolation; minimize setup/teardown overhead | session or module-scoped fixture with careful teardown | `@pytest.fixture(scope='session' or 'module')` | session-scoped database connection shared across all integration tests |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| 1. Test interaction between a service and a repository | service + real repository (or mock) | integration fixture with session or module scope; verify service calls repository correctly | `@pytest.fixture with SQLAlchemy or custom repository` | Unit tests alone don't catch bugs in cross-component interaction; integration tests verify the real integration. |
| 2. Keep a database clean between tests without manual cleanup | database + transaction rollback fixture | session starts transaction before test, rolls back after | `SQLAlchemy session with context manager` | Explicit cleanup is error-prone; transaction rollback is automatic and keeps tests isolated. |
| 3. Verify that an API request/response matches a schema | contract test (client + server schema) | contract test framework (Pact) or manual schema assertions | `jsonschema, Pact, or custom validation` | Schema misalignment causes silent failures at runtime; contract tests catch it before integration. |
| 4. Reuse expensive setup (database connection, service startup) across tests | session or module-scoped fixture | fixture with scope='session' or scope='module' and cleanup in yield | `@pytest.fixture(scope='...')` | Recreating expensive resources for each test slows down the test suite; reuse amortizes the cost. |
| 5. Test a multi-step workflow involving multiple services | integration test with real or mocked services | orchestrate service calls in test; verify final state and side effects | `pytest with integration fixtures` | Unit tests of individual services don't catch orchestration bugs; integration tests verify the whole flow. |

## Claims and their checks

- `integration-tests-verify-component-interactions`: Integration tests verify that components work together correctly across service boundaries.
- `integration-tests-are-slower-but-more-realistic`: Integration tests may hit real databases or local services, so they run slower than unit tests but catch more real-world issues.
- `fixture-scope-balances-speed-and-isolation`: Function-scoped fixtures ensure isolation; session-scoped fixtures reuse expensive setup. Choose the right scope for your trade-off.
- `transaction-rollback-keeps-db-clean`: Tests that use a database can wrap in transactions that roll back, so the database is clean for the next test.
- `contract-tests-prevent-api-misalignment`: Contract tests verify both client and server agree on request/response format, preventing integration breaks.

## Code Examples

### fleet-base: integration test with isolated_git_env fixture

```python
"""Integration test that needs a clean git environment."""
def test_commit_with_git_isolation(isolated_git_env: Path) -> None:
    # isolated_git_env is a session or module-scoped fixture
    # that sets up a temporary git config, removing global state
    import subprocess
    result = subprocess.run(['git', 'config', '--global', 'user.name'],
                            capture_output=True, text=True)
    assert result.stdout.strip() == ''  # Global config is empty
# This test verifies git behavior in isolation, without affecting the developer's real git config.

```

### fleet-ops: integration test across service boundary

```python
"""Test that a service correctly calls a repository."""
@pytest.fixture(scope='module')
def work_item_repo():
    """Module-scoped fixture: reused across all tests in this module."""
    return WorkItemRepository()

def test_dispatch_creates_work_item(work_item_repo):
    service = DispatchService(work_item_repo)
    service.dispatch(task="test_task")
    items = work_item_repo.list()
    assert len(items) == 1
    assert items[0].task == "test_task"
# The service and repository are real; this test verifies their integration.

```

### pytest: transaction rollback fixture for database tests

```python
"""Database tests with automatic rollback."""
@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    transaction.rollback()
    connection.close()

def test_insert_and_query(db_session):
    db_session.add(WorkItem(task="x"))
    items = db_session.query(WorkItem).all()
    assert len(items) == 1
# Each test inserts data; after the test, the transaction rolls back, cleaning the database.

```

### contract test: verify API schema

```python
"""Verify that an API response matches the expected schema."""
from jsonschema import validate, ValidationError

health_schema = {
    "type": "object",
    "properties": {"status": {"type": "string"}},
    "required": ["status"]
}

def test_health_endpoint_schema():
    import requests
    response = requests.get("http://localhost:8080/healthz")
    validate(instance=response.json(), schema=health_schema)
# The test verifies that the API response conforms to the contract.

```

### pytest: reuse session-scoped fixture across tests

```python
"""Session-scoped fixture shared across all tests."""
@pytest.fixture(scope='session')
def database_session():
    """Expensive setup: database connection, migrations."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()

def test_first_query(database_session):
    result = database_session.query(WorkItem).all()
    assert result == []

def test_second_query(database_session):
    # Same session as first test; reuses expensive setup
    result = database_session.query(WorkItem).all()
    assert result == []
# Both tests reuse the same database session, amortizing setup cost.

```

### fleet-base: conftest.py automatic marker assignment

```python
"""Automatic marker assignment based on directory."""
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Assign markers based on test directory (unit, integration, contract)."""
    for item in items:
        path = Path(str(item.fspath)).resolve()
        relative = path.relative_to(TESTS_ROOT.resolve())
        top_level = relative.parts[0] if relative.parts else ""

        marker_name = DIRECTORY_MARKERS.get(top_level)
        if marker_name:
            item.add_marker(getattr(pytest.mark, marker_name))
# Tests in tests/unit/ automatically get @pytest.mark.unit; tests/integration/ get @pytest.mark.integration.

```

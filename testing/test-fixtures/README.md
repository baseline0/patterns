# Test fixtures: pytest conftest patterns, scope, and dependency injection

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Open in explorer: `../../site/index.html#testing:testing-pattern:test-fixtures` (`just -f site/justfile serve`)

Pytest fixtures are reusable setup/teardown functions that tests depend on. Fixtures manage resources (databases, temporary files, mocks) and provide them to tests via dependency injection. A fixture's scope (function, class, module, session) determines when setup runs and cleanup happens. conftest.py is a pytest file that defines fixtures shared across tests in a directory and subdirectories. Fixtures compose: one fixture can depend on another, building up complex test environments from simple pieces.

## Fixtures as dependency injection for tests

A test declares its dependencies (database, mock service) as function parameters. Pytest matches parameters to fixture names and injects them. This decouples test code from setup logic and makes dependencies explicit in the test signature.

## conftest.py defines shared fixtures

conftest.py is a pytest convention file where fixtures are defined. Pytest discovers conftest.py files in the test directory and parent directories, automatically making fixtures available to all tests. This avoids importing fixtures explicitly.

## Fixture scope controls setup reuse (function, module, session)

A function-scoped fixture runs setup before each test and cleanup after. A module-scoped fixture runs setup once per module and cleans up after the module. Session-scoped fixtures run once per test session. Broader scopes reuse setup (faster) but risk test coupling; narrower scopes ensure isolation.

## Fixtures compose: one fixture depends on another

A fixture can take another fixture as a parameter. Pytest resolves the dependency chain and runs setup in order. This builds complex environments from simple pieces and avoids duplication.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `simple fixture (no dependencies, function scope)` | O(1) setup, O(1) cleanup per test | minimal overhead |
| `session-scoped fixture (reused across all tests)` | O(1) setup once; O(1) cleanup at end | expensive setup amortized across all tests |
| `fixture composition (fixture depends on another fixture)` | O(1) per dependency; resolved in order | dependency resolution is linear in dependency depth |
| `fixture with monkeypatch (patching module globals)` | O(1) patch, O(1) restore | restores patches automatically after test |
| `parameterized fixture (@pytest.fixture(params=[...]))` | O(n) where n is number of parameter values | test runs once per parameter value |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Multiple tests need the same resource (database, temporary directory, mock) | DRY: avoid duplicating setup logic in each test | fixture with @pytest.fixture decorator, injected as test parameter | `@pytest.fixture, yield for cleanup` | all tests need a temporary directory; define tmp_path fixture once |
| Setup and cleanup must happen in a specific order | Automatic teardown without explicit cleanup code | fixture with `yield` to separate setup and cleanup | `def fixture(...): setup_code; yield; cleanup_code` | start a server, yield, then stop it |
| A test depends on multiple resources (database, mock, config) | Compose fixtures; avoid deeply nested setup | fixture takes other fixtures as parameters | `def fixture_a(fixture_b, fixture_c): ...` | a service fixture depends on a database fixture and a config fixture |
| Expensive setup should be reused across tests (avoid repeating) | Balance speed (reuse) and isolation (fresh state) | session or module-scoped fixture | `@pytest.fixture(scope='module' or 'session')` | database connection or service startup, reused across tests |
| Run the same test with different parameter values | DRY: avoid copy-pasting the test | @pytest.fixture(params=[...]) or @pytest.mark.parametrize | `@pytest.fixture(params=...) or @pytest.mark.parametrize(...)` | test the same function with 5 different input values |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| 1. Multiple tests need the same temporary directory | pytest's built-in tmp_path fixture | test declares tmp_path parameter; pytest injects it | `@pytest.fixture (tmp_path is built-in)` | Avoids manual tempdir cleanup; pytest manages it. Each test gets a fresh directory. |
| 2. Setup and cleanup must be coordinated (e.g., start/stop a server) | custom fixture with yield | setup before yield; cleanup after yield | `@pytest.fixture with yield` | Cleanup is guaranteed even if the test fails; no manual try/finally needed. |
| 3. A fixture depends on another fixture (composition) | two fixtures with dependency | fixture_a takes fixture_b as parameter | `@pytest.fixture, parameter passing` | Avoids duplication; complex environments built from simple fixtures. |
| 4. Expensive setup (database) should be reused across tests | session or module-scoped fixture | @pytest.fixture(scope='session' or 'module') | `@pytest.fixture(scope=...)` | Amortizes expensive setup cost; tests run faster. |
| 5. Run the same test with 10 different inputs | parameterized fixture or parametrized test | @pytest.fixture(params=[...]) or @pytest.mark.parametrize(...) | `@pytest.fixture(params=...) or @pytest.mark.parametrize(...)` | DRY: avoid copy-pasting the test 10 times. |

## Claims and their checks

- `fixtures-are-dependency-injection-for-tests`: Fixtures inject dependencies into tests; this makes setup explicit and tests more readable.
- `conftest-py-shares-fixtures-across-tests`: Fixtures in conftest.py are automatically discovered and available to all tests in that directory and subdirectories.
- `fixture-scope-balances-reuse-and-isolation`: Function scope ensures isolation; module or session scope reuses setup. Choose the right scope for your trade-off.
- `fixtures-compose-building-complex-environments`: One fixture can depend on another; Pytest resolves the chain and runs setup in order.
- `yield-in-fixtures-simplifies-cleanup`: Using `yield` in a fixture separates setup and cleanup; code after yield runs after the test.

## Code Examples

### fleet-base: conftest.py with shared fixtures

```python
"""Shared fixtures for all tests (from fleet-base)."""
@pytest.fixture
def settings() -> Callable[..., FleetSettings]:
    def build(settings_class: type[FleetSettings] = FleetSettings, **overrides):
        return _without_process_env(settings_class)(**overrides)
    return build

def test_settings_from_overrides(settings):
    cfg = settings(api_key="secret")
    assert cfg.api_key == "secret"
# The settings fixture is defined in conftest.py; all tests can use it by declaring the parameter.

```

### pytest: fixture with setup and cleanup (yield)

```python
"""Fixture that starts a resource and cleans it up."""
@pytest.fixture
def temp_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "test_repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    yield repo  # Test runs here
    # Cleanup (if needed) happens after yield

def test_repo_exists(temp_repo):
    assert (temp_repo / ".git").exists()
# tmp_path is injected; yield provides the repo to the test; cleanup (none here) runs after.

```

### fleet-base: fixture composition (one fixture depends on another)

```python
"""Fixture that depends on another fixture."""
@pytest.fixture
def isolated_git_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    empty_config = tmp_path / "empty-gitconfig"
    empty_config.write_text("", encoding="utf-8")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(empty_config))
    return empty_config

def test_git_isolation(isolated_git_env: Path):
    # isolated_git_env depends on tmp_path and monkeypatch
    # Pytest injects them in order, then isolated_git_env
    import subprocess
    result = subprocess.run(['git', 'config', '--global', 'user.name'],
                            capture_output=True, text=True)
    assert result.stdout.strip() == ''
# tmp_path and monkeypatch are injected; isolated_git_env is constructed using them.

```

### pytest: session-scoped fixture for expensive setup

```python
"""Expensive setup reused across all tests in the session."""
@pytest.fixture(scope='session')
def database():
    """Create and migrate database once per session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

def test_first_query(database):
    session = Session(database)
    items = session.query(Item).all()
    assert items == []

def test_second_query(database):
    # Same database as first test; expensive setup not repeated
    session = Session(database)
    items = session.query(Item).all()
    assert items == []
# Both tests reuse the same database session, avoiding repeated setup.

```

### pytest: parameterized fixture

```python
"""Run a test with different parameter values."""
@pytest.fixture(params=["value1", "value2", "value3"])
def param_value(request):
    return request.param

def test_with_params(param_value):
    assert param_value in ["value1", "value2", "value3"]
# The test runs three times, once for each parameter value.

```

### fleet-base: automatic marker assignment in conftest.py

```python
"""conftest.py hook to automatically assign markers based on directory."""
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        path = Path(str(item.fspath)).resolve()
        relative = path.relative_to(TESTS_ROOT.resolve())
        top_level = relative.parts[0] if relative.parts else ""
        marker_name = DIRECTORY_MARKERS.get(top_level)
        if marker_name:
            item.add_marker(getattr(pytest.mark, marker_name))
# Conftest.py uses pytest hooks; markers are assigned based on test directory.

```

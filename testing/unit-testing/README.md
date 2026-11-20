# Unit testing: test isolation, hermetic tests, and mocking strategies

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Open in explorer: `../../site/index.html#testing:testing-pattern:unit-testing` (`just -f site/justfile serve`)

Unit tests verify single functions or classes in isolation, fast and deterministically. Hermetic tests are self-contained: they never touch external services, file systems, or databases. Mocking replaces dependencies, allowing tests to control inputs and verify behavior. Pytest markers (@pytest.mark.unit) organize tests by scope. Fixtures manage setup and teardown, keeping tests DRY.

## Isolation through dependency injection

Tests pass dependencies explicitly: a function takes a database connector as a parameter, and the test passes a mock. This breaks coupling and makes behavior testable. Avoid global state; instead, inject or monkeypatch.

## Hermetic tests: no external I/O

Hermetic tests never hit the network, disk, or external services. All I/O is mocked or replaced with in-memory stubs. A test should pass or fail the same way in isolation, in parallel, or in a different order.

## Mocking libraries: unittest.mock and pytest-mock

Mock objects replace real dependencies. unittest.mock.MagicMock records calls and returns, pytest-mock wraps it. Mocks allow tests to verify behavior without running expensive operations (database commits, HTTP calls).

## Markers partition tests by scope and runtime cost

@pytest.mark.unit tags fast, isolated tests. @pytest.mark.integration tags cross-component tests. Markers allow running only unit tests before commit (@pytest -m unit), or integration tests in CI only.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `unit test (mock dependency)` | O(1) milliseconds | isolated component, no I/O |
| `unit test setup (fixture with monkeypatch)` | O(1) setup time | in-memory fixture; minimal allocation |
| `mock assertion (verify call count, args)` | O(1) | recorded in-memory; no I/O |
| `unit test with parametrize (@pytest.mark.parametrize)` | O(n) for n inputs | same test run multiple times; linear in test count |
| `test collection (pytest discovery)` | O(n) where n is number of test files | imports all test modules; linear scan |
| `parallel unit tests (pytest-xdist, -n auto)` | O(n/p) where p is number of processes | ideal speedup if tests are independent |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Verify a single function's behavior given various inputs | O(1) milliseconds, no external calls | function under test + mock dependencies + assertions | `@pytest.fixture, unittest.mock.MagicMock, pytest-mock` | test_branch_from_result_whitespace_frozen; verify branch_from_result('   ') is None |
| Test a class constructor, field assignment, and simple methods | O(1), no I/O or network | instantiate class, set fields, call methods, assert results | `@pytest.fixture for object construction, capsys for stdout capture` | test_error_initialization; verify FleetError('msg').message == 'msg' |
| Test error handling and exception messages | O(1), verify exception type and message text | pytest.raises(ExceptionType), assert error details | `pytest.raises context manager` | test_policy_violation_includes_rule_id; verify PolicyViolation('X').rule_id == 'X' |
| Verify function calls to a mocked dependency (call count, args) | O(1), inspect mock call history | mock.assert_called_once_with(...) or mock.call_count assertions | `unittest.mock.MagicMock, pytest-mock` | verify a logger was called with the correct message |
| Run the same test on multiple inputs (parametrize) | O(n) where n is number of inputs, but DRY | @pytest.mark.parametrize with list of (input, expected) tuples | `@pytest.mark.parametrize decorator` | test_json_parse with [('{"a":1}', {'a': 1}), ('bad', ValueError)] |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| 1. Isolate a function from a database dependency | function + mock database | dependency injection (pass mock as parameter or fixture) | `unittest.mock.MagicMock or pytest-mock` | A function that queries a database cannot run fast or repeatably. Mock the database to return test data. |
| 2. Test error handling without triggering real errors | mock + exception | mock.side_effect = ExceptionType() to trigger error paths | `unittest.mock.MagicMock.side_effect` | Testing error paths without actually raising them lets tests run fast and verify both success and failure. |
| 3. Verify a function logs the correct message | mock logger + capsys | pass mock logger to function; assert mock.assert_called_with(...) | `unittest.mock.patch, pytest-mock, capsys` | Capturing logging without side effects; verify the function called log with the right args. |
| 4. Test a class that depends on an external service | class + mocked service | constructor injection (pass mock in __init__); mock returns test data | `unittest.mock.MagicMock, @pytest.fixture` | Classes that call external APIs must be testable without hitting the network; inject mocks. |
| 5. Run the same test on 10 different inputs | parametrized test | @pytest.mark.parametrize with list of (input, expected) | `@pytest.mark.parametrize decorator` | Avoids copy-pasting the same test 10 times; DRY principle for test cases. |

## Claims and their checks

- `unit-tests-run-fast`: Unit tests on isolated components run in milliseconds, not seconds, because they avoid I/O.
- `hermetic-tests-never-touch-external-services`: Hermetic tests mock all external dependencies: databases, networks, file systems, caches.
- `dependency-injection-enables-mocking`: Functions that take dependencies as parameters (not globals) can be tested with mock objects.
- `markers-enable-selective-execution`: @pytest.mark.unit and @pytest.mark.integration allow running only a subset of tests before commit.
- `mocking-is-for-external-io`: Mock external services (HTTP, database, file I/O); test real logic with real domain objects.

## Code Examples

### fleet-base: test isolation via mock dependency

```python
"""Test commit_message.attribution_lines without file I/O."""
def test_co_authored_by_trailer_fails_in_any_case(tmp_path: Path) -> None:
    path = _message(tmp_path, "fix: x\n\nco-authored-by: Someone <a@b.invalid>\n")
    assert commit_message.attribution_lines(Path(path).read_text(encoding="utf-8")) == [
        "co-authored-by: Someone <a@b.invalid>"
    ]
# The function is tested in isolation; mocking file I/O is avoided by passing text directly.

```

### fleet-base: hermetic test with monkeypatch

```python
"""A settings factory that never reads the process environment."""
@pytest.fixture
def settings() -> Callable[..., FleetSettings]:
    def build(settings_class: type[FleetSettings] = FleetSettings, **overrides):
        return _without_process_env(settings_class)(**overrides)
    return build
# The fixture isolates settings from the real environment; tests control all inputs.

```

### fleet-ops: test with mock return value

```python
"""Test branch_from_result parsing."""
def test_a_whitespace_only_result_names_no_branch() -> None:
    assert branch_from_result("   ") is None
# No mocking needed; the function is pure. Input and output are tested directly.

```

### pytest: parametrized test for multiple inputs

```python
"""Test a function on multiple inputs."""
@pytest.mark.parametrize("input_val,expected", [
    ("  ", None),
    ('{"branch": "agent/x"}', "agent/x"),
])
def test_branch_from_result(input_val: str, expected) -> None:
    assert branch_from_result(input_val) == expected
# The same test runs twice with different inputs; the test code is not duplicated.

```

### pytest: capsys to verify output without side effects

```python
"""Capture stdout/stderr to verify logging without side effects."""
def test_co_authored_by_trailer_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = _message(tmp_path, "feat: add thing\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n")
    with pytest.raises(SystemExit) as exit_info:
        commit_message.main([path])
    assert exit_info.value.code == 1
    assert "Co-Authored-By: Claude <noreply@anthropic.com>" in capsys.readouterr().err
# capsys captures output without mocking; the test verifies error messages were printed.

```

### pytest: fixture for object construction and teardown

```python
"""Fixture that constructs and tears down an object."""
@pytest.fixture
def temp_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "test_repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    yield repo
    # Cleanup is automatic after the test.
def test_repo_operations(temp_repo: Path) -> None:
    assert (temp_repo / ".git").exists()
# The fixture handles setup and teardown; tests use clean state each run.

```

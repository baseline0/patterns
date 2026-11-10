# Quiz: Test fixtures: pytest conftest patterns, scope, and dependency injection

> Generated from `content/`.

## 1. What is dependency injection in pytest?

A. Tests directly instantiate objects and pass them to fixtures
B. Tests declare parameters matching fixture names; pytest injects the fixtures
C. Tests import fixtures explicitly from a fixtures module
D. Tests call a setup function before each test

**Answer: B.** Pytest uses the test function's parameter names to match fixtures. If a test has a parameter named 'tmp_path', Pytest injects the built-in tmp_path fixture.

## 2. What is conftest.py?

A. A configuration file for pytest settings
B. A pytest file that defines shared fixtures available to all tests in that directory and subdirectories
C. A test file that runs configuration checks
D. A file that imports all test modules

**Answer: B.** conftest.py is a pytest convention; fixtures defined there are automatically discovered and available to all tests in that directory and subdirectories.

## 3. How does the `yield` keyword in a fixture work?

A. It skips the test if the condition is false
B. It returns a value from the fixture
C. It separates setup (before yield) from cleanup (after yield)
D. It makes the fixture run in parallel

**Answer: C.** yield separates setup and cleanup in a fixture. Code before yield runs before the test; code after yield runs after the test, even if the test fails.

## 4. What does fixture scope control?

A. Whether the fixture is visible in other test files
B. When setup runs and when cleanup happens (function, module, session)
C. How many tests can use the fixture
D. The order in which tests run

**Answer: B.** Fixture scope determines: function-scoped fixtures run before each test; module-scoped fixtures run once per module; session-scoped fixtures run once per session.

## 5. How can a fixture depend on another fixture?

A. By importing it explicitly
B. By calling it directly
C. By declaring the other fixture as a parameter
D. By registering it in conftest.py

**Answer: C.** A fixture can take another fixture as a parameter. Pytest resolves the dependency chain and runs setup in order.

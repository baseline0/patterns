# Quiz: Unit testing: test isolation, hermetic tests, and mocking strategies

> Generated from `content/`.

## 1. Why should unit tests avoid calling external services like databases or APIs?

A. External services are always slower, so tests must be fast
B. Tests should be hermetic: deterministic, fast, and runnable in any order or location
C. External services are not available in the test environment
D. All of the above

**Answer: B.** Hermetic tests are isolated and reproducible. They run in milliseconds, in any order, and don't depend on network or service availability.

## 2. Which pytest marker should a fast, isolated test declare?

A. @pytest.mark.integration
B. @pytest.mark.unit
C. @pytest.mark.slow
D. @pytest.mark.skip

**Answer: B.** @pytest.mark.unit tags fast, isolated component tests. Markers allow running only unit tests before commit with `pytest -m unit`.

## 3. What does unittest.mock.MagicMock.side_effect do?

A. Records how many times the mock was called
B. Defines the return value of the mock
C. Raises an exception or returns a value when the mock is called
D. Prevents the mock from being called more than once

**Answer: C.** side_effect can be an exception (raises it) or a callable (calls it). This lets tests trigger error paths without raising real errors.

## 4. In dependency injection, what is passed to the function being tested?

A. The real external service
B. A mock object that simulates the service
C. A stub that returns a default value
D. Both mock and stub objects

**Answer: B.** Mocks replace real dependencies in tests, allowing control over inputs and verification of behavior without side effects.

## 5. What does @pytest.mark.parametrize do?

A. Skips a test until it passes
B. Runs a test multiple times with different inputs
C. Marks a test as slow or expensive
D. Enables parallel test execution

**Answer: B.** Parametrize runs the same test function with different arguments, specified as a list of tuples. This keeps tests DRY.

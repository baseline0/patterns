# Testing patterns

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

Each topic has a write-up, a quiz, and an HTML page. The topics:

- [Contract testing: API contracts and consumer-driven contracts](contract-testing/README.md): quiz in `contract-testing/quiz_guide.md`
- [Integration testing: service boundaries, fixture lifecycle, and database tests](integration-testing/README.md): quiz in `integration-testing/quiz_guide.md`
- [Test fixtures: pytest conftest patterns, scope, and dependency injection](test-fixtures/README.md): quiz in `test-fixtures/quiz_guide.md`
- [Unit testing: test isolation, hermetic tests, and mocking strategies](unit-testing/README.md): quiz in `unit-testing/quiz_guide.md`

## Use it

- Regenerate every output: `uv run python testing/tools/build.py`
- Test the claims and the outputs: `uv run pytest tests/unit/test_testing_patterns.py`
- Flashcards for Anki: `flashcards.csv`

# Contributing

Thanks for your interest in contributing to this repository! By contributing, you agree that your contributions will be licensed under the project's MIT License.

## How to contribute

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-change`.
3. Make your changes in that branch.
4. Add tests (if applicable) and update documentation.
5. Run the example and any tests locally.
6. Commit and push your changes, then open a pull request against `main`.

## Reporting issues

If you find a bug or want to request a feature, open a GitHub issue describing the problem or desired improvement and include a minimal reproducible example where appropriate.

## Code style

- Follow idiomatic Python (PEP 8).
- Use type hints where helpful.
- Use `black` or your preferred formatter for consistent styling.

## Patterns and data files

- If you're adding or improving pattern files, place them in the `patterns/` directory.
- Add both YAML and JSON variants where appropriate and keep regexes well-documented.

## Tests

- Although there are currently no tests committed, we welcome tests written with `pytest`.
- Add tests under a `tests/` directory and include instructions in the PR description.

## Running the example

1. Install dependencies: `pip install -r requirements.txt`
2. Run the example script (if present) to validate patterns and behavior.

## Pull request guidelines

- Make small, focused changes per PR.
- Include a clear description of what and why.
- Link related issues.

## License

This project is released under the MIT License. By contributing you accept that your contributions will be licensed under the same.

## Thank you

Thanks for helping improve this project!
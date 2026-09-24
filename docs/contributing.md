# Contributing to rsync-s

Thank you for your interest in contributing to `rsync-s`! 

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:
- Be respectful and inclusive.
- Focus on technical merit.
- Avoid personal attacks.

## Development Workflow

1. **Fork the repository**: Create your own fork of the project.
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Implement changes**: Follow the existing code style and include tests.
4. **Write tests**: Every new feature must be accompanied by a corresponding test in `tests/`.
5. **Commit your changes**: `git commit -m "feat: description of your change"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Submit a Pull Request**: Open a PR against the `main` branch.

## Testing Standards

We use `pytest` for all testing. 
- Tests must be idempotent.
- Tests must not depend on external system state (use `tempfile` where possible).
- All tests must pass before a PR is considered for merging.

## Style Guide

- Follow PEP 8 for Python code.
- Use clear, descriptive variable and function names.
- Document complex logic with docstrings.
- Use descriptive commit messages (e.g., `feat:`, `fix:`, `docs:`, `test:`).

## License

This project is licensed under the MIT License.

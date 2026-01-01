# Contributing to AutoDev Studio

Thank you for your interest in contributing to AutoDev Studio! We welcome contributions from developers, researchers, and enthusiasts.

## 🤝 How to Contribute

### 1. Reporting Bugs
- Open an issue on GitHub.
- clearly describe the issue, including steps to reproduce.
- Attach any relevant logs from `workspace/logs/`.

### 2. Suggesting Enhancements
- Open an issue with the tag `enhancement`.
- Describe the feature and the problem it solves.
- Reference the `PRODUCT_DESIGN_DOC.md` if it aligns with the roadmap.

### 3. Submitting Pull Requests
1. **Fork** the repository.
2. **Clone** your fork locally.
3. Create a new **branch** (`git checkout -b feature/amazing-feature`).
4. **Implement** your changes.
   - Ensure checks pass: `pytest tests/`
   - Ensure code is formatted (PEP8).
5. **Commit** your changes with descriptive messages.
6. **Push** to your branch.
7. Open a **Pull Request** targeting the `main` branch.

## 🏗️ Project Structure

- `src/core`: The heart of the system (Orchestrator, SOP Engine). **Requires careful review.**
- `src/agents`: Role definitions. Easier to extend with new personas.
- `src/ui`: The Streamlit dashboard.
- `tests`: Integration and Unit tests.

## 🧪 Testing

We use `pytest` for testing. Run the full suite before submitting:
```bash
pytest tests/
```

## 📜 License
By contributing, you agree that your contributions will be licensed under the MIT License defined in `LICENSE`.

**Happy Coding!** 🚀

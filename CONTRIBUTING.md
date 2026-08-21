# Contributing to skill-doctor

Thank you for considering contributing! This document outlines the process.

## Ways to Contribute

- **Report bugs**: Open an issue using the Bug Report template
- **Improve documentation**: Submit PRs for typos, clarity, or missing content
- **Submit a pitfall**: Help grow `references/坑库.md` with new failure patterns
- **Submit code**: Fix bugs or implement features via PR

## Development Process

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes**: Follow existing code style and conventions
4. **Regression test** (required before any PR):
   - `python scripts/selftest.py` — good fixtures green, bad fixtures caught per rule
   - `python scripts/trigger_eval.py` — description trigger families
   - `python scripts/audit.py .` — self static audit must stay clean
5. **Commit**: Use [Conventional Commits](https://www.conventionalcommits.org/) format
6. **Push**: `git push origin feature/your-feature`
7. **Open a Pull Request**: Fill in the PR template completely

## PR Guidelines

- Keep changes focused: one PR = one logical change
- Update relevant documentation if your change affects user-facing behavior
- Reference related issues in the PR description (`Fixes #123`)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Questions?

Open a [Discussion](https://github.com/hyt315/skill-doctor/discussions) or use the Question issue template.

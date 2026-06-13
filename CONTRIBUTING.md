# Contributing to kre8

Thanks for your interest in contributing to kre8. This document covers how to get started.

## Before You Start

kre8 is a focused project with a narrow scope — a Thinking Infrastructure Engine that translates natural-language intent into policy-validated infrastructure design. Contributions that stay within that scope are most likely to be accepted. If you're unsure whether something fits, open an issue first.

## How to Contribute

### Reporting Bugs

Open a GitHub issue with:
- A clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs or error output

### Suggesting Features

Open a GitHub issue tagged `enhancement`. Describe the problem you're solving, not just the solution. Given kre8's design-first architecture, proposals that include a design rationale are more likely to move forward.

### Submitting Code

1. Fork the repo and create a branch from `main`.
2. Branch naming: `feat/short-description`, `fix/short-description`, `docs/short-description`.
3. Keep changes focused — one logical change per PR.
4. Run existing tests before submitting. Add tests for new behavior.
5. Open a pull request against `main` with a clear description of what and why.

## Branch naming

Use the same type prefixes as commit messages:

| Prefix | Use for |
|---|---|
| `feat/` | New features or behaviour |
| `fix/` | Bug fixes |
| `docs/` | Documentation only |
| `test/` | Test additions or fixes |
| `chore/` | Tooling, config, dependencies, repo maintenance |
| `refactor/` | Code restructuring with no behaviour change |

Format: `type/short-description` — lowercase, hyphens, no spaces.

Examples:
- `feat/webhook-configure-modal`
- `fix/mid-stream-halt-codex`
- `docs/update-runbook-auth-steps`
- `chore/coderabbit-config`

One branch per logical change. Keep branches short-lived — open a PR, merge, delete.

## Commit style

This project follows [Conventional Commits](https://www.conventionalcommits.org). Format: `type(scope): description` in plain imperative present tense. Scope is the module name when it fits.

Common types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`. Examples:
- `fix(bug): handle clean halt during fan-out`
- `feat(app): add collapse-all to turn cards`
- `docs(examples): add directive injection screenshot`
- `chore: update .gitignore glob for .DS_Store`

## Development Setup

```bash
git clone https://github.com/klokworkai/kre8.git
cd kre8
pip install -r requirements.txt
```

Tests:
```bash
pytest stub_tests/
pytest integration_tests/
```

## Licensing

By submitting a contribution, you agree that your contribution is licensed under the [Apache License 2.0](LICENSE). No CLA required — the license handles it.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

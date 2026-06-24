# Changelog

All notable changes to kre8 will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
kre8 uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial OSS release setup (LICENSE, NOTICE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY)
- i2d2 orchestrator: FastAPI `/health` + `POST /process`, Kit extraction wired
- konnekt: full LLM adapter with 5-family MODEL_REGISTRY, ROLE_DEFAULTS, GCP Secret Manager, DeepSeek fallback
- Kit, Kraph, and Kanvas schemas (`i2d2/schemas.py`) with Pydantic validation

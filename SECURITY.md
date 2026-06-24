# Security Policy

## Supported Versions

kre8 is currently in early development. Security fixes are applied to the latest version on `main` only.

| Version | Supported |
|---------|-----------|
| latest (main) | ✅ |
| older commits | ❌ |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities by emailing [kre8@klokwork.ai](mailto:kre8@klokwork.ai). Include:

- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested mitigations (optional)

You can expect an acknowledgement within 48 hours and a status update within 7 days. We will coordinate disclosure timing with you before publishing any fix publicly.

## Scope

Areas of particular interest:

- LLM prompt injection or output manipulation affecting infrastructure synthesis
- Policy gate bypass in konform/OPA integration
- Secrets leakage via konnekt or GCP Secret Manager integration
- Unsafe HCL generation that could result in destructive infrastructure changes

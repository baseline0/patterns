# Provider mappings

Vendor-agnostic pattern first, provider details second. `content/*.yaml` maps a pattern to AWS, Azure, and GCP services,
a local emulator, and a plan-only Terraform fixture. `tools/build.py` renders `matrix.md`, `index.html`, and
`glossary.json`, and it fails when a declared fixture is missing.

```bash
just -f providers/justfile build
just -f providers/justfile check
```

Fixtures under `terraform/{aws,azure,gcp}/` are for `terraform init`, `validate`, and `plan` only. They must not deploy.

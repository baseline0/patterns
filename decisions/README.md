# Decision records

Practice architecture decision records against the committed examples in `docs/adr/`. The coach prompts for context,
options, decision, and consequences, then reveals the real record.

```bash
just -f decisions/justfile list
just -f decisions/justfile drill 0001-circuit-breaker-after-b2
just -f decisions/justfile prompts
```

# CLAUDE.md

Agent economy simulation: LLM agents spend energy to earn credits, alone (tier 1) or in negotiated pairs (tier 2), and die at zero energy.

## References
- Plan doc: "Agent economy simulation: v0.1 plan" (read with the Claude Docs tools)
- Tasks: GitHub issues T1–T17 in harimp/agentopia. Each lists the features it covers, its dependencies and when it is done; unit tests are part of every ticket's definition of done.

## Stack
- Python 3.12+ (`.python-version` pins 3.14), managed with uv
- Async runtime: stdlib `asyncio`
- Tests: pytest + pytest-asyncio (`asyncio_mode = "auto"`, so async tests need no marker)
- Config: TOML read with stdlib `tomllib`
- Planned by later tickets: SQLite store (T2), local models through Ollama (T7)

## Commands
```sh
uv sync          # install the project and dev dependencies
uv run pytest    # run tests
```

## Layout
```
config/default.toml        v0.1 defaults
src/agentopia/config/
  base.py                  ConfigError, to_amount (Decimal, 2 places)
  world.py                 WorldConfig
  tier.py                  TierConfig
  config.py                Config: loads TOML, orchestrates the config types
tests/                     pytest tests
```

## Conventions
- One config type per module, each a frozen dataclass with its own `from_dict()` and `validate()`; `Config.load(path)` orchestrates them.
- Invalid or missing config values raise `ConfigError`.
- Credits and energy are `Decimal` values with 2 decimal places, never floats.

## Commits
Follow [Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <summary>`, e.g. `feat(config): ...`.
- Body: a short paragraph on the purpose of the task or commit, then the changes as a concise bullet list.
- Footer: reference the ticket, e.g. `Closes #1`.

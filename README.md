# agentopia
Agent-populated civilization simulation tool

## About
Scenario v0.1 tests one question: under configurable rules, can AI agents come up with ways to thrive?

- Agents spend **energy** to earn **credits**, and die when their energy reaches zero.
- Tier 1 work is done alone and breaks even: 1 energy for 1 credit.
- Tier 2 work is done in pairs and profits: 2 energy for 3 credits, split as the two agents negotiate.
- Every action costs 0.1 energy. Credits buy energy at 1:1, up to an energy cap.
- Agents run concurrently on local models through Ollama. Every action goes through a single world engine and is stored in SQLite.

## Status
- [x] T1 · Project scaffold and configuration

## Setup
Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
```

## Configuration
Run settings live in a TOML file. `config/default.toml` holds the v0.1 defaults: agent count, energy cap, starting balances, exchange rate, action cost, end condition and tier payoffs.

```sh
uv run python -c "from agentopia.config import Config; print(Config.load('config/default.toml'))"
```

## Tests
```sh
uv run pytest
```

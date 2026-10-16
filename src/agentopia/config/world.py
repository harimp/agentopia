"""World settings: agent count, balances, rates, costs and end condition."""

from dataclasses import dataclass
from decimal import Decimal

from agentopia.config.base import ConfigError, to_amount


@dataclass(frozen=True)
class WorldConfig:
    MIN_AGENTS = 3
    MAX_AGENTS = 25
    END_CONDITIONS = frozenset({"all_dead"})

    agent_count: int
    energy_cap: Decimal
    starting_energy: Decimal
    starting_credits: Decimal
    exchange_rate: Decimal
    action_cost: Decimal
    end_condition: str

    @classmethod
    def from_dict(cls, raw: dict) -> "WorldConfig":
        world = cls(
            agent_count=int(raw["agent_count"]),
            energy_cap=to_amount(raw["energy_cap"]),
            starting_energy=to_amount(raw["starting_energy"]),
            starting_credits=to_amount(raw["starting_credits"]),
            exchange_rate=to_amount(raw["exchange_rate"]),
            action_cost=to_amount(raw["action_cost"]),
            end_condition=str(raw["end_condition"]),
        )
        world.validate()
        return world

    def validate(self) -> None:
        if not self.MIN_AGENTS <= self.agent_count <= self.MAX_AGENTS:
            raise ConfigError(f"agent_count must be {self.MIN_AGENTS} to {self.MAX_AGENTS}")
        for name in ("energy_cap", "exchange_rate"):
            if getattr(self, name) <= 0:
                raise ConfigError(f"{name} must be positive")
        for name in ("starting_energy", "starting_credits", "action_cost"):
            if getattr(self, name) < 0:
                raise ConfigError(f"{name} must not be negative")
        if self.starting_energy > self.energy_cap:
            raise ConfigError("starting_energy must not exceed energy_cap")
        if self.end_condition not in self.END_CONDITIONS:
            raise ConfigError(f"end_condition must be one of {sorted(self.END_CONDITIONS)}")

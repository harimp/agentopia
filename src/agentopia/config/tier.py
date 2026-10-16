"""Production tier payoffs."""

from dataclasses import dataclass
from decimal import Decimal

from agentopia.config.base import ConfigError, to_amount


@dataclass(frozen=True)
class TierConfig:
    AGENTS_PER_TIER = {1: 1, 2: 2}

    number: int
    agents: int
    energy_cost: Decimal
    credits: Decimal

    @classmethod
    def from_dict(cls, number: int, raw: dict) -> "TierConfig":
        tier = cls(
            number=number,
            agents=int(raw["agents"]),
            energy_cost=to_amount(raw["energy_cost"]),
            credits=to_amount(raw["credits"]),
        )
        tier.validate()
        return tier

    def validate(self) -> None:
        expected = self.AGENTS_PER_TIER.get(self.number)
        if expected is None:
            raise ConfigError(f"unknown tier {self.number}")
        if self.agents != expected:
            raise ConfigError(f"tier {self.number} must have {expected} agents")
        if self.energy_cost <= 0 or self.credits <= 0:
            raise ConfigError(f"tier {self.number} costs and payoffs must be positive")

"""Top-level run configuration loaded from a TOML file."""

import tomllib
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from agentopia.config.base import ConfigError
from agentopia.config.tier import TierConfig
from agentopia.config.world import WorldConfig


@dataclass(frozen=True)
class Config:
    world: WorldConfig
    tiers: dict[int, TierConfig]

    @classmethod
    def load(cls, path: str | Path) -> "Config":
        with open(path, "rb") as f:
            return cls.from_dict(tomllib.load(f, parse_float=Decimal))

    @classmethod
    def from_dict(cls, raw: dict) -> "Config":
        try:
            config = cls(
                world=WorldConfig.from_dict(raw["world"]),
                tiers={int(n): TierConfig.from_dict(int(n), t) for n, t in raw["tiers"].items()},
            )
        except KeyError as e:
            raise ConfigError(f"missing config value: {e.args[0]}") from None
        config.validate()
        return config

    def validate(self) -> None:
        if self.tiers.keys() != TierConfig.AGENTS_PER_TIER.keys():
            raise ConfigError(f"tiers must be exactly {sorted(TierConfig.AGENTS_PER_TIER)}")

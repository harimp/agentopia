import asyncio
from decimal import Decimal
from pathlib import Path

import pytest

from agentopia.config import Config, ConfigError

DEFAULT = Path(__file__).parent.parent / "config" / "default.toml"


def write_config(tmp_path, replace=None):
    text = DEFAULT.read_text()
    for old, new in (replace or {}).items():
        assert old in text
        text = text.replace(old, new)
    path = tmp_path / "config.toml"
    path.write_text(text)
    return path


def test_defaults_match_plan():
    config = Config.load(DEFAULT)
    world = config.world
    assert world.agent_count == 6
    assert world.energy_cap == Decimal("100.00")
    assert world.starting_energy == Decimal("50.00")
    assert world.starting_credits == Decimal("50.00")
    assert world.exchange_rate == Decimal("1.00")
    assert world.action_cost == Decimal("0.10")
    assert world.end_condition == "all_dead"
    assert config.tiers[1].agents == 1
    assert config.tiers[1].energy_cost == Decimal("1")
    assert config.tiers[1].credits == Decimal("1")
    assert config.tiers[2].agents == 2
    assert config.tiers[2].energy_cost == Decimal("2")
    assert config.tiers[2].credits == Decimal("3")


def test_override_changes_values(tmp_path):
    path = write_config(tmp_path, {"energy_cap = 100.00": "energy_cap = 80.5"})
    assert Config.load(path).world.energy_cap == Decimal("80.50")


def test_amounts_round_to_two_places(tmp_path):
    path = write_config(tmp_path, {"action_cost = 0.1": "action_cost = 0.123"})
    assert Config.load(path).world.action_cost == Decimal("0.12")


@pytest.mark.parametrize(
    "old, new",
    [
        ("agent_count = 6", "agent_count = 2"),
        ("agent_count = 6", "agent_count = 26"),
        ("energy_cap = 100.00", "energy_cap = 0"),
        ("exchange_rate = 1", "exchange_rate = 0"),
        ("action_cost = 0.1", "action_cost = -0.1"),
        ("starting_energy = 50", "starting_energy = 150"),
        ('end_condition = "all_dead"', 'end_condition = "never"'),
        ("agents = 2", "agents = 3"),
        ("credits = 3", "credits = 0"),
        ("[tiers.2]", "[tiers.3]"),
        ("agent_count = 6", ""),
    ],
)
def test_invalid_config_raises(tmp_path, old, new):
    with pytest.raises(ConfigError):
        Config.load(write_config(tmp_path, {old: new}))


async def test_async_runtime():
    assert await asyncio.sleep(0, result=1) == 1

"""Shared helpers for config types."""

from decimal import Decimal

CENT = Decimal("0.01")


class ConfigError(ValueError):
    """Raised when a config file is missing values or holds invalid ones."""


def to_amount(value) -> Decimal:
    """Credits and energy are decimals with up to 2 places."""
    return Decimal(value).quantize(CENT)

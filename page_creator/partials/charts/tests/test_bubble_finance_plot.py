import pytest
from page_creator.partials.charts.bubble_finance_plot import _format_amount


@pytest.mark.parametrize(
    "value, expected",
    [
        # Below 1K — no suffix
        (0, "€0"),
        (1, "€1"),
        (847, "€847"),
        (999, "€999"),
        # Exact thresholds — no decimal
        (1_000, "€1K"),
        (10_000, "€10K"),
        (100_000, "€100K"),
        (1_000_000, "€1M"),
        (10_000_000, "€10M"),
        (1_000_000_000, "€1B"),
        # With decimal
        (1_500, "€1.5K"),
        (94_300, "€94.3K"),
        (4_823_150, "€4.8M"),
        (2_100_000_000, "€2.1B"),
        # Rounds correctly at .x0
        (1_100_000, "€1.1M"),
        (1_050_000, "€1.1M"),  # rounds up at .05
    ],
)
def test_format_amount(value: float, expected: str) -> None:
    assert _format_amount(value) == expected

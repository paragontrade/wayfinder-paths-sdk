"""HIP3_DEXES validation on ActivePerpsStrategy subclasses."""

from pathlib import Path

import pytest

from wayfinder_paths.core.strategies.active_perps import ActivePerpsStrategy

_APEX_DIR = Path(__file__).parent.parent / "strategies" / "apex_gmx_velocity"


def _define_strategy(dexes: list[str]) -> type[ActivePerpsStrategy]:
    return type(
        "Hip3DexStrategy",
        (ActivePerpsStrategy,),
        {
            "REF": _APEX_DIR / "backtest_ref.json",
            "SIGNAL": "wayfinder_paths.strategies.apex_gmx_velocity.signal:compute_signal",
            "HIP3_DEXES": dexes,
        },
    )


@pytest.mark.parametrize(
    "dex", ["xyz", "flx", "vntl", "hyna", "km", "abcd", "cash", "para", "mkts", "io"]
)
def test_live_hip3_dex_is_accepted(dex):
    cls = _define_strategy([dex])
    assert cls.HIP3_DEXES == [dex]


def test_unknown_hip3_dex_is_rejected():
    with pytest.raises(RuntimeError, match="unknown dex 'notadex'"):
        _define_strategy(["notadex"])

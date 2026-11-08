from __future__ import annotations

import typing as t

import pytest

from blinker import Signal


@pytest.mark.parametrize("inner_raises", [False, True])
def test_nested_muted_keeps_outer_scope_muted(inner_raises: bool) -> None:
    signal = Signal()
    received = []

    def receiver(sender: t.Any) -> None:
        received.append(sender)

    signal.connect(receiver)
    with signal.muted():
        try:
            with signal.muted():
                signal.send("inner")
                if inner_raises:
                    raise ValueError("inner failure")
        except ValueError:
            pass
        signal.send("outer")
        assert signal.is_muted
    signal.send("after")
    assert received == ["after"]


def test_muted_preserves_preexisting_state() -> None:
    signal = Signal()
    signal.is_muted = True
    with signal.muted():
        assert signal.is_muted
    assert signal.is_muted

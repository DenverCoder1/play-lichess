import play_lichess
from play_lichess.constants import TimeMode, Variant, Color

import pytest


def test_real_time():
    match = play_lichess.real_time()
    assert match.time_mode == TimeMode.REALTIME
    assert len(match.link) == len("https://lichess.org/12345678")
    assert match.title == "Rapid (5+8) casual Chess • Open challenge • lichess.org"
    assert match.color == Color.RANDOM
    assert match.variant == Variant.STANDARD


def test_real_time_custom():
    match = play_lichess.real_time(
        minutes=6, increment=0, variant=Variant.ANTICHESS, color=Color.WHITE
    )
    assert match.time_mode == TimeMode.REALTIME
    assert len(match.link) == len("https://lichess.org/12345678")
    assert (
        match.title
        == "Blitz (6+0) Antichess casual Chess • Open challenge • lichess.org"
    )
    assert match.color == Color.WHITE
    assert match.variant == Variant.ANTICHESS


def test_correspondence():
    match = play_lichess.correspondence()
    assert match.time_mode == TimeMode.CORRESPONDENCE
    assert len(match.link) == len("https://lichess.org/12345678")
    assert match.title == "Correspondence casual Chess • Open challenge • lichess.org"
    assert match.color == Color.RANDOM
    assert match.variant == Variant.STANDARD


def test_correspondence_custom():
    match = play_lichess.correspondence(
        days=3, variant=Variant.ATOMIC, color=Color.BLACK
    )
    assert match.time_mode == TimeMode.CORRESPONDENCE
    assert len(match.link) == len("https://lichess.org/12345678")
    assert (
        match.title
        == "Correspondence Atomic casual Chess • Open challenge • lichess.org"
    )
    assert match.color == Color.BLACK
    assert match.variant == Variant.ATOMIC


def test_unlimited():
    match = play_lichess.unlimited()
    assert match.time_mode == TimeMode.UNLIMITED
    assert len(match.link) == len("https://lichess.org/12345678")
    assert match.title == "Correspondence casual Chess • Open challenge • lichess.org"
    assert match.color == Color.RANDOM
    assert match.variant == Variant.STANDARD
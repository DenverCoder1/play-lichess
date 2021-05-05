import play_lichess
from play_lichess.constants import TimeMode, Variant, Color
from play_lichess.exceptions import BadArgumentError

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


def test_real_time_invalid_minutes():
    with pytest.raises(BadArgumentError):
        play_lichess.real_time(
            minutes=0, increment=0, variant=Variant.ANTICHESS, color=Color.WHITE
        )


def test_real_time_invalid_increment():
    with pytest.raises(BadArgumentError):
        play_lichess.real_time(
            minutes=0, increment=-1, variant=Variant.ANTICHESS, color=Color.WHITE
        )


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


def test_real_time_invalid_days():
    with pytest.raises(BadArgumentError):
        play_lichess.correspondence(
            days=0, variant=Variant.ANTICHESS, color=Color.WHITE
        )


def test_unlimited():
    match = play_lichess.unlimited()
    assert match.time_mode == TimeMode.UNLIMITED
    assert len(match.link) == len("https://lichess.org/12345678")
    assert match.title == "Correspondence casual Chess • Open challenge • lichess.org"
    assert match.color == Color.RANDOM
    assert match.variant == Variant.STANDARD


def test_create():
    match = play_lichess.create()
    assert match.time_mode == TimeMode.REALTIME
    assert len(match.link) == len("https://lichess.org/12345678")
    assert match.title == "Rapid (5+8) casual Chess • Open challenge • lichess.org"
    assert match.color == Color.RANDOM
    assert match.variant == Variant.STANDARD


def test_create_correspondence():
    match = play_lichess.create(TimeMode.CORRESPONDENCE)
    assert match.time_mode == TimeMode.CORRESPONDENCE
    assert len(match.link) == len("https://lichess.org/12345678")
    assert match.title == "Correspondence casual Chess • Open challenge • lichess.org"
    assert match.color == Color.RANDOM
    assert match.variant == Variant.STANDARD


def test_create_unlimited():
    match = play_lichess.create(TimeMode.UNLIMITED)
    assert match.time_mode == TimeMode.UNLIMITED
    assert len(match.link) == len("https://lichess.org/12345678")
    assert match.title == "Correspondence casual Chess • Open challenge • lichess.org"
    assert match.color == Color.RANDOM
    assert match.variant == Variant.STANDARD


def test_create_custom():
    match = play_lichess.create(
        TimeMode.CORRESPONDENCE, variant=Variant.HORDE, color=Color.BLACK, days=3
    )
    assert match.time_mode == TimeMode.CORRESPONDENCE
    assert len(match.link) == len("https://lichess.org/12345678")
    assert (
        match.title
        == "Correspondence Horde casual Chess • Open challenge • lichess.org"
    )
    assert match.color == Color.BLACK
    assert match.variant == Variant.HORDE

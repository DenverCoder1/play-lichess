from play_lichess import main
from play_lichess.constants import Color, TimeMode, Variant


def test_real_time():
    data = main.__get_form_data()
    expected = {
        "variant": 1,
        "fen": "",
        "timeMode": 1,
        "time": 5,
        "increment": 8,
        "days": 2,
        "color": "random",
        "level": None,
    }
    assert data == expected


def test_real_time_custom():
    data = main.__get_form_data(
        minutes=6, increment=0, variant=Variant.ANTICHESS, color=Color.WHITE
    )
    expected = {
        "variant": 6,
        "fen": "",
        "timeMode": 1,
        "time": 6,
        "increment": 0,
        "days": 2,
        "color": "white",
        "level": None,
    }
    assert data == expected


def test_correspondence():
    data = main.__get_form_data(time_mode=TimeMode.CORRESPONDENCE)
    expected = {
        "variant": 1,
        "fen": "",
        "timeMode": 2,
        "time": 5,
        "increment": 8,
        "days": 2,
        "color": "random",
        "level": None,
    }
    assert data == expected


def test_correspondence_custom():
    data = main.__get_form_data(
        time_mode=TimeMode.CORRESPONDENCE,
        minutes=6,
        increment=0,
        variant=Variant.ANTICHESS,
        color=Color.WHITE,
    )
    expected = {
        "variant": 6,
        "fen": "",
        "timeMode": 2,
        "time": 6,
        "increment": 0,
        "days": 2,
        "color": "white",
        "level": None,
    }
    assert data == expected


def test_unlimited():
    data = main.__get_form_data(time_mode=TimeMode.UNLIMITED)
    expected = {
        "variant": 1,
        "fen": "",
        "timeMode": 0,
        "time": 5,
        "increment": 8,
        "days": 2,
        "color": "random",
        "level": None,
    }
    assert data == expected


def test_ai():
    data = main.__get_form_data(ai_level=3)
    expected = {
        "variant": 1,
        "fen": "",
        "timeMode": 1,
        "time": 5,
        "increment": 8,
        "days": 2,
        "color": "random",
        "level": 3,
    }
    assert data == expected

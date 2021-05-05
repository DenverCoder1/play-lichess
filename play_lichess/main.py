from typing import Any, Dict, Optional
import requests
from requests.models import Response

from .constants import Color, TimeMode, Variant
from .exceptions import BadArgumentError, HttpError
from .match import Match


def __get_html_title(response: Response) -> str:
    """Returns the title content of the response text given the Response"""
    text = response.text
    start = text.find("<title>") + len("<title>")
    end = text.find("</title>")
    return text[start:end]


def __get_form_data(
    time_mode: TimeMode = TimeMode.REALTIME,
    variant: Variant = Variant.STANDARD,
    color: Color = Color.RANDOM,
    minutes: float = 5,
    increment: int = 8,
    days: int = 2,
    ai_level: Optional[int] = None,
) -> Dict[str, Any]:
    return {
        "variant": variant.data,
        "fen": "",
        "timeMode": time_mode.data,
        "time": minutes,  # only for real time
        "increment": increment,  # only for real time
        "days": days,  # only for correspondence
        "level": ai_level,  # only for AI games
        "color": color.data,
    }


def create(
    time_mode: TimeMode = TimeMode.REALTIME,
    variant: Variant = Variant.STANDARD,
    color: Color = Color.RANDOM,
    minutes: float = 5,
    increment: int = 8,
    days: int = 2,
    ai_level: Optional[int] = None,
) -> Match:
    """Start a match that two players can join
    This method allows parameters for Real-Time, Correspondence, or Unlimited matches

    :param time_mode: :class:`TimeMode`
        The time mode of the match (REALTIME, CORRESPONDENCE, or UNLIMITED)
    :param variant: :class:`Variant`
        The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
    :param color: :class:`Color`
        The color that will be assigned to the first player that joins (WHITE, BLACK, or RANDOM)
    :param minutes: :class:`float`
        The number of minutes for the match when time_mode is REALTIME
    :param increment: :class:`int`
        Amount of seconds to increment the clock each turn when time_mode is REALTIME
    :param days: :class:`int`
        The number of days for the match when time_mode is CORRESPONDENCE
    :param ai_level: Optional[:class:`int`]
        'None' to play with a friend or Stockfish Level 1-8 to play against AI
    """

    # validate parameters
    if minutes <= 0:
        raise BadArgumentError("'minutes' must be a positive number")
    if not isinstance(increment, int) or increment < 0:
        raise BadArgumentError("'increment' must be a non-negative whole number")
    if not isinstance(days, int) or days <= 0:
        raise BadArgumentError("'days' must be a positive whole number")

    # request match
    endpoint_url = "https://lichess.org/"
    endpoint_url += "setup/friend" if not ai_level else "setup/ai"
    data = __get_form_data(
        time_mode, variant, color, minutes, increment, days, ai_level
    )
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.post(endpoint_url, data=data, headers=headers)

    # get the title from the response
    title = __get_html_title(response)

    # get redirect url for the match
    redirect_url = response.url

    # throw an error if the url did not redirect to a match
    if redirect_url == endpoint_url:
        raise HttpError(
            response.status_code, response.reason, endpoint_url, response.text
        )

    return Match(title, redirect_url, variant, time_mode, color)


def real_time(
    minutes: float = 5,
    increment: int = 8,
    variant: Variant = Variant.STANDARD,
    color: Color = Color.RANDOM,
    ai_level: Optional[int] = None,
) -> Match:
    """Start a live match that two players can join

    :param minutes: :class:`float`
        The number of minutes for the match (excluding increment)
    :param increment: :class:`int`
        Amount of seconds to increment the clock each turn
    :param variant: :class:`Variant`
        The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
    :param color: :class:`Color`
        The color that will be assigned to the first player that joins (WHITE, BLACK, or RANDOM)
    :param ai_level: Optional[:class:`int`]
        'None' to play with a friend or Stockfish Level 1-8 to play against AI
    """
    return create(
        time_mode=TimeMode.REALTIME,
        variant=variant,
        color=color,
        minutes=minutes,
        increment=increment,
        ai_level=ai_level,
    )


def correspondence(
    days: int = 2,
    variant: Variant = Variant.STANDARD,
    color: Color = Color.RANDOM,
    ai_level: Optional[int] = None,
) -> Match:
    """Start a correspondence match that two players can join

    :param days: :class:`int`
        The number of days for the match
    :param variant: :class:`Variant`
        The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
    :param color: :class:`Color`
        The color that will be assigned to the first player that joins (WHITE, BLACK, or RANDOM)
    :param ai_level: Optional[:class:`int`]
        'None' to play with a friend or Stockfish Level 1-8 to play against AI
    """
    return create(
        time_mode=TimeMode.CORRESPONDENCE,
        variant=variant,
        color=color,
        days=days,
        ai_level=ai_level,
    )


def unlimited(
    variant: Variant = Variant.STANDARD,
    color: Color = Color.RANDOM,
    ai_level: Optional[int] = None,
) -> Match:
    """Start a unlimited time match that two players can join

    :param variant: :class:`Variant`
        The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
    :param color: :class:`Color`
        The color that will be assigned to the first player that joins (WHITE, BLACK, or RANDOM)
    :param ai_level: Optional[:class:`int`]
        'None' to play with a friend or Stockfish Level 1-8 to play against AI
    """
    return create(
        time_mode=TimeMode.UNLIMITED,
        variant=variant,
        color=color,
        ai_level=ai_level,
    )

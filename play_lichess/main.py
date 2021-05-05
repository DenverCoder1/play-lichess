import requests
from requests.models import Response

from .constants import Color, TimeMode, Variant
from .exceptions import BadArgumentError, HttpError
from .match import Match


def __create_match(
    time_mode: TimeMode,
    variant: Variant,
    color: Color,
    minutes: float = 5,
    increment: int = 8,
    days: int = 2,
) -> Match:
    """Create an invite for a new game on Lichess
    Return a match containing the link and additional information
    """

    endpoint_url = "https://lichess.org/setup/friend"
    data = {
        "variant": variant.data,
        "fen": "",
        "timeMode": time_mode.data,
        "time": minutes,  # only for real time
        "increment": increment,  # only for real time
        "days": days,  # only for correspondence
        "color": color.data,
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.post(
        endpoint_url,
        data=data,
        headers=headers,
    )

    # get the title from the response
    title = __get_html_title(response)

    # get redirect url for the match
    redirect_url = response.url

    # check that the url was redirected to a game url
    if redirect_url == endpoint_url:
        raise HttpError(
            response.status_code, response.reason, endpoint_url, response.text
        )

    return Match(title, redirect_url, variant, time_mode, color)


def __get_html_title(response: Response) -> str:
    """Returns the title content of the response text given the Response"""
    text = response.text
    start = text.find("<title>") + len("<title>")
    end = text.find("</title>")
    return text[start:end]


def real_time(
    minutes: float = 5,
    increment: int = 8,
    variant: Variant = Variant.STANDARD,
    color: Color = Color.RANDOM,
) -> Match:
    """Start a live match that two players can join

    :param minutes: :class:`float`
        The number of minutes for the match (excluding increment)
    :param increment: :class:`int`
        Amount of seconds to increment the clock each turn
    :param variant: :class:`Variant`
        The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
    :param color: :class:`Color`
        The color that will be assigned to the first player to join the match
    """
    if minutes <= 0:
        raise BadArgumentError("'minutes' must be a positive number")
    if not isinstance(increment, int) or increment < 0:
        raise BadArgumentError("'increment' must be a non-negative whole number")
    return __create_match(
        time_mode=TimeMode.REALTIME,
        variant=variant,
        color=color,
        minutes=minutes,
        increment=increment,
    )


def correspondence(
    days: int = 2,
    variant: Variant = Variant.STANDARD,
    color: Color = Color.RANDOM,
) -> Match:
    """Start a correspondence match that two players can join

    :param days: :class:`int`
        The number of days for the match
    :param variant: :class:`Variant`
        The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
    :param color: :class:`Color`
        The color that will be assigned to the first player to join the match
    """
    if not isinstance(days, int) or days <= 0:
        raise BadArgumentError("'minutes' must be a positive whole number")
    return __create_match(
        time_mode=TimeMode.CORRESPONDENCE,
        variant=variant,
        color=color,
        days=days,
    )


def unlimited(
    variant: Variant = Variant.STANDARD,
    color: Color = Color.RANDOM,
) -> Match:
    """Start a unlimited time match that two players can join

    :param variant: :class:`Variant`
        The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
    :param color: :class:`Color`
        The color that will be assigned to the first player to join the match
    """
    return __create_match(
        time_mode=TimeMode.UNLIMITED,
        variant=variant,
        color=color,
    )

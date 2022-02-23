import json
from dataclasses import dataclass
from typing import Any, Coroutine, Optional

import aiohttp

from .exceptions import BadArgumentError, HttpError
from .types import Color, TimeControl, TimeMode, User, Variant


@dataclass
class Match:
    """Class for storing results about a created match link

    Attributes
    ----------
    challenge_id: :class:`str`
        The challenge id of the match
    challenge_url: :class:`str`
        The url of the match
    status: :class:`str`
        The status of the match
    challenger: Optional[:class:`str`]
        The challenger of the match
    dest_user: Optional[:class:`str`]
        The destination user of the match
    variant: :class:`Variant`
        The variant of the match
    rated: :class:`bool`
        Whether the match is rated
    speed: :class:`TimeMode`
        The speed of the match
    time_control: :class:`TimeControl`
        The time control of the match
    color: :class:`Color`
        The color of the player who starts the match
    url_white: :class:`str`
        The url of the white player
    url_black: :class:`str`
        The url of the black player
    """

    challenge_id: str
    challenge_url: str
    status: str
    challenger: Optional[User] = None
    dest_user: Optional[User] = None
    variant: Variant = Variant.STANDARD
    rated: bool = False
    speed: TimeMode = TimeMode.CORRESPONDENCE
    time_control: Optional[TimeControl] = None
    color: Color = Color.RANDOM
    url_white: Optional[str] = None
    url_black: Optional[str] = None
    name: Optional[str] = None
    _data: Optional[dict] = None

    @classmethod
    def from_data(cls: "Match", data: dict, name: Optional[str] = None) -> "Match":
        """Create a :class:`Match` object from a dictionary of data

        Parameters
        ----------
        data: :class:`dict`
            A dictionary of data to create the :class:`Match` object from
        name: Optional[:class:`str`]
            The name of the match

        Returns
        -------
        :class:`Match`
            A :class:`Match` object with the data from the dictionary
        """
        return cls(
            challenge_id=data["challenge"]["id"],
            challenge_url=data["challenge"]["url"],
            status=data["challenge"]["status"],
            challenger=(
                User.from_data(data["challenge"]["challenger"])
                if data["challenge"]["challenger"]
                else None
            ),
            dest_user=(
                User.from_data(data["challenge"]["destUser"])
                if data["challenge"]["destUser"]
                else None
            ),
            variant=Variant.find_by_data(data["challenge"]["variant"]["key"]),
            rated=data["challenge"]["rated"],
            speed=TimeMode.find_by_data(data["challenge"]["speed"]),
            time_control=TimeControl.from_data(data["challenge"]["timeControl"]),
            color=Color.find_by_data(data["challenge"]["color"]),
            url_white=data["urlWhite"],
            url_black=data["urlBlack"],
            name=name,
            _data=data,
        )

    @classmethod
    async def create(
        cls: "Match",
        *,
        rated: bool = False,
        clock_limit: Optional[int] = 300,
        clock_increment: Optional[int] = 0,
        days: Optional[int] = None,
        variant: Variant = Variant.STANDARD,
        fen: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Coroutine[Any, Any, "Match"]:
        """Start a match that two players can join

        :param rated: :class:`bool`
            Game is rated and impacts players ratings
        :param clock_limit: :class:`int`
            Clock initial time in seconds. Leave blank for a correspondence or unlimited match.
            If specified, must be between 0 and 10800 seconds.
        :param clock_increment: :class:`int`
            Clock increment in seconds. Leave blank for a correspondence or unlimited match.
            If specified, must be between 0 and 180 seconds.
        :param days: :class:`int`
            Days per turn for correspondence matches. Leave blank for a live or unlimited match.
            If specified, must be between 1, 2, 3, 5, 7, 10, or 14 days.
        :param variant: :class:`Variant`
            The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
            The default is STANDARD
        :param fen: :class:`str`
            Custom initial position (in FEN). Variant must be standard, and the game cannot be rated.
            The default position is "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        :param name: :class:`str`
            Optional name for the challenge that players will see on the challenge page.

        Returns
        -------
        :class:`Match`
            A :class:`Match` object with the data from the API

        Raises
        ------
        :class:`BadArgumentError`
            If days is set and clock_limit or clock_increment is also set.
            If one of clock_limit or clock_increment is set but the other is not.
        :class:`HttpError`
            If the HTTP request fails, for example:
            If clock_limit or clock_increment is not in the valid range.
            If clock_limit and clock_increment are both set to 0.
            If days is not in the valid range.
            If rated is set, but there is no time control.
            If a rate-limit or server error occurs.
        """
        if days and (clock_limit or clock_increment):
            raise BadArgumentError(
                "days cannot be set with clock_limit or clock_increment"
            )
        if not days and (clock_limit is None) ^ (clock_increment is None):
            raise BadArgumentError(
                "Both clock_limit and clock_increment must be specified or neither"
            )
        if fen is not None:
            if variant != Variant.STANDARD:
                raise BadArgumentError(
                    "fen can only be specified for STANDARD variants"
                )
            if rated:
                raise BadArgumentError("fen can only be specified for unrated games")

        endpoint_url = "https://lichess.org/api/challenge/open"
        params = {
            "rated": rated,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "variant": variant.value.data,
            "days": days,
            "fen": fen,
            "name": name,
        }
        data = json.dumps({k: v for k, v in params.items() if v is not None})
        headers = {"User-Agent": "play-lichess", "Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint_url, data=data, headers=headers
            ) as response:
                if response.status != 200:
                    raise HttpError(
                        status_code=response.status,
                        reason=response.reason,
                        endpoint=endpoint_url,
                        response_text=await response.json(),
                    )
                return cls.from_data(await response.json(), name)


class RealTimeMatch(Match):
    @classmethod
    async def create(
        cls: "RealTimeMatch",
        *,
        rated: bool = False,
        clock_limit: Optional[int] = 300,
        clock_increment: Optional[int] = 0,
        variant: Variant = Variant.STANDARD,
        fen: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Coroutine[Any, Any, "Match"]:
        return await super().create(
            rated=rated,
            clock_limit=clock_limit,
            clock_increment=clock_increment,
            variant=variant,
            fen=fen,
            name=name,
        )


class CorrespondenceMatch(Match):
    @classmethod
    async def create(
        cls: "CorrespondenceMatch",
        *,
        rated: bool = False,
        days: Optional[int] = 1,
        variant: Variant = Variant.STANDARD,
        fen: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Coroutine[Any, Any, "Match"]:
        return await super().create(
            rated=rated,
            clock_limit=None,
            clock_increment=None,
            days=days,
            variant=variant,
            fen=fen,
            name=name,
        )


class UnlimitedMatch(Match):
    @classmethod
    async def create(
        cls: "UnlimitedMatch",
        *,
        variant: Variant = Variant.STANDARD,
        fen: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Coroutine[Any, Any, "Match"]:
        return await super().create(
            rated=False,
            clock_limit=None,
            clock_increment=None,
            days=None,
            variant=variant,
            fen=fen,
            name=name,
        )

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping, Type, TypeVar

import aiohttp

from .exceptions import BadArgumentError, HttpError
from .types import Color, TimeControl, TimeMode, User, Variant

MatchInfoT = TypeVar("MatchInfoT", bound="MatchInfo")

if TYPE_CHECKING:
    from typing import Literal

    _NumberOfDays = Literal[1, 2, 3, 5, 7, 10, 14]


@dataclass
class MatchInfo:
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
    name: Optional[:class:`str`]
        The name of the match
    """

    challenge_id: str
    challenge_url: str
    status: str
    challenger: User | None = None
    dest_user: User | None = None
    variant: Variant = Variant.STANDARD
    rated: bool = False
    speed: TimeMode = TimeMode.CORRESPONDENCE
    time_control: TimeControl | None = None
    color: Color = Color.RANDOM
    url_white: str | None = None
    url_black: str | None = None
    name: str | None = None
    _data: Mapping[str, Any] | None = None

    @classmethod
    def from_data(
        cls: Type[MatchInfoT], data: Mapping[str, Any], name: str | None = None
    ) -> MatchInfoT:
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
    async def _create_match(
        cls: Type[MatchInfoT],
        *,
        rated: bool = False,
        clock_limit: int | None = 300,
        clock_increment: int | None = 0,
        days: int | None = None,
        variant: Variant = Variant.STANDARD,
        fen: str | None = None,
        name: str | None = None,
    ) -> MatchInfoT:
        """Start a match that two players can join. This method is called by the create methods of the subclasses."""
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


class Match(MatchInfo):
    """Subclass of :class:`MatchInfo` for creating matches of any type"""

    @classmethod
    async def create(
        cls: Type["Match"],
        *,
        rated: bool = False,
        clock_limit: int | None = 300,
        clock_increment: int | None = 0,
        days: _NumberOfDays | None = None,
        variant: Variant = Variant.STANDARD,
        fen: str | None = None,
        name: str | None = None,
    ) -> "Match":
        """Start a match that two players can join

        Parameters
        ----------
        rated: :class:`bool`
            Game is rated and impacts players ratings
        clock_limit: Optional[:class:`int`]
            Clock initial time in seconds. Leave blank for a correspondence or unlimited match.
            If specified, must be between 0 and 10800 seconds.
        clock_increment: Optional[:class:`int`]
            Clock increment in seconds. Leave blank for a correspondence or unlimited match.
            If specified, must be between 0 and 180 seconds.
        days: Optional[:class:`int`]
            Days per turn for correspondence matches. Leave blank for a live or unlimited match.
            If specified, must be 1, 2, 3, 5, 7, 10, or 14 days.
        variant: :class:`Variant`
            The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
            The default is STANDARD
        fen: :class:`str`
            Custom initial position (in FEN). Variant must be standard, and the game cannot be rated.
            The default position is "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        name: :class:`str`
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
        return await super()._create_match(
            rated=rated,
            clock_limit=clock_limit,
            clock_increment=clock_increment,
            days=days,
            variant=variant,
            fen=fen,
            name=name,
        )


class RealTimeMatch(MatchInfo):
    """Subclass of :class:`MatchInfo` for creating real-time matches"""

    @classmethod
    async def create(
        cls: Type["RealTimeMatch"],
        *,
        rated: bool = False,
        clock_limit: int = 300,
        clock_increment: int = 0,
        variant: Variant = Variant.STANDARD,
        fen: str | None = None,
        name: str | None = None,
    ) -> "RealTimeMatch":
        """Start a real-time match that two players can join

        Parameters
        ----------
        rated: :class:`bool`
            Game is rated and impacts players ratings
        clock_limit: :class:`int`
            Clock initial time in seconds. Must be between 0 and 10800 seconds.
        clock_increment: :class:`int`
            Clock increment in seconds. Must be between 0 and 180 seconds.
        variant: :class:`Variant`
            The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
            The default is STANDARD
        fen: :class:`str`
            Custom initial position (in FEN). Variant must be standard, and the game cannot be rated.
            The default position is "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        name: :class:`str`
            Optional name for the challenge that players will see on the challenge page.

        Returns
        -------
        :class:`RealTimeMatch`
            A :class:`RealTimeMatch` object with the data from the API

        Raises
        ------
        :class:`BadArgumentError`
            If None is passed to one of clock_limit or clock_increment.
        :class:`HttpError`
            If the HTTP request fails, for example:
            If clock_limit or clock_increment is not in the valid range.
            If clock_limit and clock_increment are both set to 0.
            If rated is set, but there is no time control.
            If a rate-limit or server error occurs.
        """
        return await super()._create_match(
            rated=rated,
            clock_limit=clock_limit,
            clock_increment=clock_increment,
            variant=variant,
            fen=fen,
            name=name,
        )


class CorrespondenceMatch(MatchInfo):
    """Subclass of :class:`MatchInfo` for creating correspondence matches"""

    @classmethod
    async def create(
        cls: Type["CorrespondenceMatch"],
        *,
        rated: bool = False,
        days: _NumberOfDays = 1,
        variant: Variant = Variant.STANDARD,
        fen: str | None = None,
        name: str | None = None,
    ) -> "CorrespondenceMatch":
        """Start a correspondence match that two players can join

        Parameters
        ----------
        rated: :class:`bool`
            Game is rated and impacts players ratings
        days: Optional[:class:`int`]
            Days per turn for correspondence matches. Must be 1, 2, 3, 5, 7, 10, or 14 days.
        variant: :class:`Variant`
            The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
            The default is STANDARD
        fen: :class:`str`
            Custom initial position (in FEN). Variant must be standard, and the game cannot be rated.
            The default position is "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        name: :class:`str`
            Optional name for the challenge that players will see on the challenge page.

        Returns
        -------
        :class:`CorrespondenceMatch`
            A :class:`CorrespondenceMatch` object with the data from the API

        Raises
        ------
        :class:`HttpError`
            If the HTTP request fails, for example:
            If days is not in the valid range.
            If rated is set, but there is no time control.
            If a rate-limit or server error occurs.
        """
        return await super()._create_match(
            rated=rated,
            clock_limit=None,
            clock_increment=None,
            days=days,
            variant=variant,
            fen=fen,
            name=name,
        )


class UnlimitedMatch(MatchInfo):
    """Subclass of :class:`MatchInfo` for creating unlimited matches"""

    @classmethod
    async def create(
        cls: Type["UnlimitedMatch"],
        *,
        variant: Variant = Variant.STANDARD,
        fen: str | None = None,
        name: str | None = None,
    ) -> "UnlimitedMatch":
        """Start an unlimited match that two players can join

        Parameters
        ----------
        variant: :class:`Variant`
            The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
            The default is STANDARD
        fen: :class:`str`
            Custom initial position (in FEN). Variant must be standard, and the game cannot be rated.
            The default position is "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        name: :class:`str`
            Optional name for the challenge that players will see on the challenge page.

        Returns
        -------
        :class:`UnlimitedMatch`
            A :class:`UnlimitedMatch` object with the data from the API

        Raises
        ------
        :class:`HttpError`
            If the HTTP request fails, for example:
            If a rate-limit or server error occurs.
        """
        return await super()._create_match(
            rated=False,
            clock_limit=None,
            clock_increment=None,
            days=None,
            variant=variant,
            fen=fen,
            name=name,
        )

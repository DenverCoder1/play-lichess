from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .option import Option


class Variant(Option, Enum):
    """Lichess chess variants"""

    STANDARD = Option("Standard", "standard")
    CRAZYHOUSE = Option("Crazyhouse", "crazyhouse")
    CHESS960 = Option("Chess 960", "chess960")
    KING_OF_THE_HILL = Option("King of the Hill", "kingOfTheHill")
    THREE_CHECK = Option("Three-check", "threeCheck")
    ANTICHESS = Option("Antichess", "antichess")
    ATOMIC = Option("Atomic", "atomic")
    HORDE = Option("Horde", "horde")
    RACING_KINGS = Option("Racing Kings", "racingKings")


class TimeMode(Option, Enum):
    """Lichess time modes / speeds"""

    ULTRABULLET = Option("Ultra-Bullet", "ultraBullet")
    BULLET = Option("Bullet", "bullet")
    BLITZ = Option("Blitz", "blitz")
    RAPID = Option("Rapid", "rapid")
    CLASSICAL = Option("Classical", "classical")
    CORRESPONDENCE = Option("Correspondence", "correspondence")


class Color(Option, Enum):
    """Lichess possible colors for the first player to join a match"""

    WHITE = Option("White", "white")
    BLACK = Option("Black", "black")
    RANDOM = Option("Random", "random")


class TimeControlType(Option, Enum):
    """Lichess time control types"""

    UNLIMITED = Option("Unlimited", "unlimited")
    CLOCK = Option("Clock", "clock")


@dataclass
class TimeControl:
    """
    Class representing a time control

    Attributes
    ----------

    type: :class:`TimeControlType`
        The type of time control (clock or unlimited)
    limit: Optional[:class:`int`]
        The clock time limit in seconds if real-time
    increment: Optional[:class:`int`]
        The clock increment in seconds if real-time
    show: Optional[:class:`str`]
        The time control string for display (eg. "5+2")
    """

    type: TimeControlType
    limit: Optional[int]
    increment: Optional[int]
    show: Optional[str]

    @classmethod
    def from_data(cls: "TimeControl", data: dict) -> "TimeControl":
        """Create a time control from a dictionary"""
        return cls(
            type=TimeControlType.find_by_data(data["type"]),
            limit=data.get("limit", None),
            increment=data.get("increment", None),
            show=data.get("show", None),
        )


@dataclass
class User:
    """
    Class to represent a Lichess user

    Attributes
    ----------

    id: str
        The user's Lichess ID
    name: str
        The user's Lichess username
    online: Optional[bool]
        Whether the user is online
    provisional: Optional[bool]
        Whether the user is provisional
    rating: Optional[:class:`int`]
        The user's Lichess rating
    title: Optional[:class:`str`]
        The user's Lichess title
    """

    id: str
    name: str
    online: Optional[bool]
    provisional: Optional[bool]
    rating: Optional[int]
    title: Optional[str]

    @classmethod
    def from_data(cls: "User", data: dict) -> "User":
        """Create a :class:`User` object from a dictionary of data

        Parameters
        ----------
        data: :class:`dict`
            A dictionary of data to create the :class:`User` object from

        Returns
        -------
        :class:`User`
            A :class:`User` object with the data from the dictionary
        """
        return cls(
            id=data["id"],
            name=data["username"],
            online=data.get("online", None),
            provisional=data.get("provisional", None),
            rating=data.get("rating", None),
            title=data.get("title", None),
        )

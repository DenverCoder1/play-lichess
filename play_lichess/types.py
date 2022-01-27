from dataclasses import dataclass
from typing import Optional
from .option import Option
from enum import Enum


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
    """Lichess time modes"""

    ULTRABULLET = Option("Ultra-Bullet", "ultraBullet")
    BULLET = Option("Bullet", "bullet")
    BLITZ = Option("Blitz", "blitz")
    RAPID = Option("Rapid", "rapid")
    CLASSICAL = Option("Classical", "classical")
    CORRESPONDENCE = Option("Correspondence", "correspondence")


class Color(Option, Enum):
    """Lichess possible player 1 colors"""

    WHITE = Option("White", "white")
    BLACK = Option("Black", "black")
    RANDOM = Option("Random", "random")


class TimeControlType(Option, Enum):
    """Lichess time modes"""

    UNLIMITED = Option("Unlimited", "unlimited")
    CLOCK = Option("Clock", "clock")


@dataclass
class TimeControl:
    """
    Attributes
    ----------

    type: :class:`TimeControlType`
        The type of time control (clock or unlimited)
    limit: Optional[:class:`int`]
        The clock time limit in seconds
    increment: Optional[:class:`int`]
        The clock increment in seconds
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
    online: bool
        Whether the user is online
    provisional: bool
        Whether the user is provisional
    rating: int
        The user's Lichess rating
    title: str
        The user's Lichess title
    """

    id: str
    name: str
    online: bool
    provisional: bool
    rating: int
    title: str

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
            online=data["online"],
            provisional=data["provisional"],
            rating=data["rating"],
            title=data["title"],
        )

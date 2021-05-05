from .option import Option
from enum import Enum


class Variant(Option, Enum):
    """Lichess chess variants"""

    STANDARD = Option("Standard", 1)
    CRAZYHOUSE = Option("Crazyhouse", 10)
    CHESS960 = Option("Chess 960", 2)
    KING_OF_THE_HILL = Option("King of the Hill", 4)
    THREE_CHECK = Option("Three-check", 5)
    ANTICHESS = Option("Antichess", 6)
    ATOMIC = Option("Atomic", 7)
    HORDE = Option("Horde", 8)
    RACING_KINGS = Option("Racing Kings", 9)
    FROM_POSITION = Option("From Position", 3)


class TimeMode(Option, Enum):
    """Lichess time modes"""

    REALTIME = Option("Real-time", 1)
    CORRESPONDENCE = Option("Correspondence", 2)
    UNLIMITED = Option("Unlimited", 0)


class Color(Option, Enum):
    """Lichess possible player 1 colors"""

    WHITE = Option("White", "white")
    BLACK = Option("Black", "black")
    RANDOM = Option("Random", "random")

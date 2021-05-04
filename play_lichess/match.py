from dataclasses import dataclass
from .constants import Color, TimeMode, Variant


@dataclass
class Match:
    """Class for storing results about a created match link

    Attributes
    ----------
    title: :class:`str`
        The page title of the generated match link
    link: :class:`str`
        The invite URL of the match
    variant: :class:`Variant`
        The variant of the match (STANDARD, ANTICHESS, CHESS960, etc.)
    time_mode: :class:`TimeMode`
        The time mode of the match (REALTIME, CORRESPONDENCE, or UNLIMITED)
    color: :class:`Color`
        The color that will be assigned to the first player to join the match
    """

    title: str
    link: str
    variant: Variant
    time_mode: TimeMode
    color: Color

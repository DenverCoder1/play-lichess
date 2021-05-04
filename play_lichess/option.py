from typing import TypeVar

T = TypeVar("T")


class Option:
    """Class for storing a pair with a name and a value

    Attributes
    ----------
    name: :class:`str`
        A human-readable string representing the option
    value: :class:`T`
        The internal value of the option for API usage
    """

    def __init__(self, name: str, value: T):
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> T:
        return self.__value

    def __str__(self):
        return self.name

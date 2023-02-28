from __future__ import annotations

from typing import Any, NamedTuple, Type, TypeVar

OptionT = TypeVar("OptionT", bound="Option")


class Option(NamedTuple):
    """Base class for options. All subclasses should inherit from this class and Enum."""

    description: str
    data: Any

    def __str__(self):
        return self.description

    @classmethod
    def find_by_description(cls: Type[OptionT], description: str) -> OptionT:
        """Get an option from a description

        Examples:

        - ``Variant.find_by_description("Antichess")``
        - ``Color.find_by_description("White")``
        - ``TimeMode.find_by_description("Real-time")``

        Parameters
        ----------
        description: :class:`str`
            The description of the option

        Returns
        -------
        :class:`Option`
            The option with the description

        Raises
        ------
        ValueError
            If the description is not found
        """
        for option in cls:  # type: ignore  # must be an Enum
            if description == option.description:
                return option
        raise ValueError("Unknown option")

    @classmethod
    def find_by_data(cls: Type[OptionT], data: str) -> OptionT:
        """Get an option from its data

        Examples:

        - ``Variant.find_by_data("antichess")``
        - ``Color.find_by_data("white")``
        - ``TimeMode.find_by_data("ultraBullet")``

        Parameters
        ----------
        data: :class:`str`
            The data of the option

        Returns
        -------
        :class:`Option`
            The option with the data

        Raises
        ------
        ValueError
            If the option doesn't exist
        """
        for option in cls:  # type: ignore  # must be an Enum
            if data == option.data:
                return option
        raise ValueError("Unknown option")

    @classmethod
    def find(cls: Type[OptionT], key: str) -> OptionT:
        """Get an option from description or data

        Examples:

        - ``Variant.find("Antichess")``
        - ``Variant.find("ultraBullet")``
        - ``TimeMode.find("Real-time")``
        - ``TimeMode.find("realTime")``

        Parameters
        ----------
        key: :class:`str`
            The description or data of the option

        Returns
        -------
        :class:`Option`
            The option with the description or data

        Raises
        ------
        ValueError
            If the option doesn't exist
        """
        try:
            return cls.find_by_description(key)
        except ValueError:
            return cls.find_by_data(key)

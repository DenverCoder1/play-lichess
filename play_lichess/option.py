from typing import List, NamedTuple, TypeVar

T = TypeVar("T")


class Option(NamedTuple):
    description: str
    data: T

    def __str__(self):
        return self.description

    @classmethod
    def find_by_description(cls, description: str) -> "Option":
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
        options: List[Option] = list(cls)
        for option in options:
            if description == option.description:
                return option
        raise ValueError("Unknown option")

    @classmethod
    def find_by_data(cls, data: str) -> "Option":
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
        options: List[Option] = list(cls)
        for option in options:
            if data == option.data:
                return option
        raise ValueError("Unknown option")

    @classmethod
    def find(cls, key: str) -> "Option":
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

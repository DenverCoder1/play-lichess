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
        ``Variant.find_by_description("Antichess")``
        ``Color.find_by_description("White")``
        ``TimeMode.find_by_description("Real-time")``
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
        ``Variant.find_by_data("antichess")``
        ``Color.find_by_data("white")``
        ``TimeMode.find_by_data("ultraBullet")``
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
        ``Variant.find("Antichess")``
        ``Variant.find("ultraBullet")``
        ``TimeMode.find("Real-time")``
        ``TimeMode.find("realTime")``
        """
        try:
            return cls.find_by_description(key)
        except ValueError:
            return cls.find_by_data(key)

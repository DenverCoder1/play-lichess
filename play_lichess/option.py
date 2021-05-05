from typing import List, NamedTuple, TypeVar

T = TypeVar("T")


class Option(NamedTuple):
    description: str
    data: T

    def __str__(self):
        return self.description

    @classmethod
    def find(cls, description: str) -> "Option":
        """Get an option from a description

        Examples:
        ``Variant.find("Antichess")``
        ``Color.find("White")``
        ``TimeMode.find("Real-time")``
        """
        options: List[Option] = list(cls)
        for option in options:
            if description == option.description:
                return option
        raise ValueError("Unknown option")

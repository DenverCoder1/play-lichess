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
        eg. `Variant.from_description("Antichess")`
        """
        options: List[Option] = list(cls)
        for option in options:
            if description == option.description:
                return option
        raise ValueError("Unknown option")

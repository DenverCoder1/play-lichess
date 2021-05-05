from collections import namedtuple


class Option(namedtuple("Option", ["description", "data"])):
    def __str__(self):
        return self.description

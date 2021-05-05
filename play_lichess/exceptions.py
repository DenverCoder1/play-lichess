class BaseError(RuntimeError):
    """Base exception for exceptions caused by this package"""

    @property
    def message(self):
        raise NotImplementedError

    def __str__(self):
        return self.message


class HttpError(BaseError):
    """Exception caused by requests that were unsuccessful"""

    def __init__(
        self, status_code: int, reason: str, endpoint: str, response_text: str
    ):
        self.status_code = status_code
        self.reason = reason
        self.endpoint = endpoint
        self.response_text = response_text

    @property
    def message(self):
        return f"{self.status_code} {self.reason} {self.endpoint}"


class BadArgumentError(BaseError):
    """Exception caused by invalid arguments"""

    def __init__(self, description: str):
        self.description = description

    @property
    def message(self):
        return self.description

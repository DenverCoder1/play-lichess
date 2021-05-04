class HttpException(Exception):
    """Class for exceptions caused by requests that were unsuccessful"""

    def __init__(
        self, status_code: int, reason: str, endpoint: str, response_text: str
    ):
        self.status_code = status_code
        self.reason = reason
        self.endpoint = endpoint
        self.response_text = response_text

    def __str__(self):
        return f"{self.status_code} {self.reason} {self.endpoint}"

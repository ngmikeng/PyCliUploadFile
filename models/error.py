

class ErrorResponse:
    error: bool
    message: str
    payload: dict

    def __init__(self, error, message, payload):
        self.error = error
        self.message = message
        self.payload = payload

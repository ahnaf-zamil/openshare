class AppException(Exception):
    def __init__(self, http_return_code, msg: str = ""):
        self.http_return_code = http_return_code
        self.message = msg

    http_return_code: int
    message: str = ""

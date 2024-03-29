from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    message: str | None = "Base API Exception"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message

        super().__init__(status_code=self.status_code, detail=self.message)

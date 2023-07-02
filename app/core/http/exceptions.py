from fastapi import status, HTTPException


class HTTP_400_BadRequestError(HTTPException):
    def __init__(self, detail: str = "", headers: dict[str, str] | None = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers
        )


class HTTP_401_UnauthorizedError(HTTPException):
    def __init__(self, detail: str = "", headers: dict[str, str] | None = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers
        )


class HTTP_403_ForbiddenError(HTTPException):
    def __init__(self, detail: str = "", headers: dict[str, str] | None = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail, headers=headers
        )


class HTTP_404_NotFoundError(HTTPException):
    def __init__(self, detail: str = "", headers: dict[str, str] | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers
        )


class HTTP_409_ConflictError(HTTPException):
    def __init__(self, detail: str = "", headers: dict[str, str] | None = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, detail=detail, headers=headers
        )

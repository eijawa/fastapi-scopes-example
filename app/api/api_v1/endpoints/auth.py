from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.core.contrib.auth import authenticate, register
from app.core.contrib.auth import exceptions as AuthExceptions
from app.core.http.exceptions import (
    HTTP_400_BadRequestError,
    HTTP_401_UnauthorizedError,
    HTTP_403_ForbiddenError,
    HTTP_409_ConflictError,
)
from app.core.security import Token, TokenData, create_access_token
from app.schemas.user import CreateUserSchema
from app.crud.repositories import UsersPermissionsRepository
from app.core.settings import settings

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Пользователь ввёл неверные данные для авторизации!"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Выбраны недоступные текущему пользователю права!"
        },
        status.HTTP_403_FORBIDDEN: {"description": "Пользователь заблокирован!"},
    },
)
async def login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(db_session),
) -> Token:
    try:
        user = authenticate(session, credentials=login_data)
    except AuthExceptions.BadCredentialsError:
        # Пользователь ввёл неверные данные для авторизации
        raise HTTP_400_BadRequestError(
            detail="Пользователь ввёл неверные данные для авторизации!"
        )
    except AuthExceptions.UserBlockedError:
        # Пользователь заблокирован
        raise HTTP_403_ForbiddenError(detail="Пользователь заблокирован!")

    if not UsersPermissionsRepository.has(
        session, user=user, permissions=login_data.scopes
    ):
        raise HTTP_401_UnauthorizedError(
            "Выбраны недоступные текущему пользователю права!"
        )

    access_token = create_access_token(
        TokenData(id=user.id, username=user.username, scopes=login_data.scopes)
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    response_description="Регистрация прошла успешно. Пользователь создан",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Произошла непредвиденная ошибка!"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Пользователь с таким `username` уже существует!"
        },
    },
)
async def registration(
    register_data: CreateUserSchema, session: Session = Depends(db_session)
) -> Response:
    try:
        register(session, credentials=register_data)
    except SQLAlchemyExceptions.IntegrityError:
        # Пользователь с таким username уже существует!
        raise HTTP_409_ConflictError("Пользователь с таким username уже существует!")
    except Exception as e:
        if settings.DEBUG:
            raise HTTP_400_BadRequestError(str(e))
        else:
            # Произошла непредвиденная ошибка!
            raise HTTP_400_BadRequestError("Произошла непредвиденная ошибка!")

    return Response(status_code=status.HTTP_201_CREATED)

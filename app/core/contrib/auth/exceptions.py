class BadCredentialsError(Exception):
    """
    Ошибка, возникающая при использовании некорретных данных авторизации
    """

    ...


class MaxRetriesReachedError(Exception):
    """
    Ошибка, возникающая при превышении попыток входа
    """

    ...


class UserBlockedError(Exception):
    """
    Ошибка, возникающая при блокировке пользователя
    """

    ...

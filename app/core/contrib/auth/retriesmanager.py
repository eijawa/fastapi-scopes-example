from collections import UserDict

from app.core.settings import settings

from .exceptions import MaxRetriesReachedError


class RetriesManager(UserDict):
    """
    Менеджер неудачных попыток входа в аккаунт.

    Позже его внутренности можно будет заменить на кручение Redis
    """

    def increase(self, key: int) -> None:
        if key not in self.data:
            self.data[key] = 0

        self.data[key] += 1

        if self.data[key] >= settings.MAX_RETRIES_COUNT:
            raise MaxRetriesReachedError()
        
    def purify(self, key: int) -> None:
        if key in self.data:
            del self.data[key]


retries_manager = RetriesManager()

from abc import ABC, abstractmethod
from datetime import datetime


class IAccessTradeProvider(ABC):

    @abstractmethod
    def has_access_now(self) -> bool:
        raise NotImplementedError

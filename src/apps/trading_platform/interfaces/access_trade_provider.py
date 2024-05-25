from abc import ABC, abstractmethod


class IAccessTradeProvider(ABC):

    @abstractmethod
    def has_access_now(self) -> bool:
        raise NotImplementedError

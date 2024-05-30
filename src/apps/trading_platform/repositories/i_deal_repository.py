from abc import ABC, abstractmethod

from src.apps.trading_platform.models import DealSettings


class IDealRepository(ABC):
    @abstractmethod
    def get_deal_by_id_or_none(self, deal_id: int) -> DealSettings | None:
        """Fetch a deal from the database by its ID."""
        raise NotImplementedError

    @abstractmethod
    def get_all_deals(self) -> list[DealSettings]:
        """Fetch all deals from the database."""
        raise NotImplementedError

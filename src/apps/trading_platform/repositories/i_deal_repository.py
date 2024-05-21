from abc import ABC, abstractmethod
from typing import List
from src.apps.trading_platform.models import DealSettings


class IDealRepository(ABC):
    @abstractmethod
    def get_deal_by_id(self, deal_id: int) -> DealSettings:
        """Fetch a deal from the database by its ID."""
        raise NotImplementedError("Method get_deal_by_id() must be implemented")

    @abstractmethod
    def get_all_deals(self) -> List[DealSettings]:
        """Fetch all deals from the database."""
        raise NotImplementedError("Method get_all_deals() must be implemented")

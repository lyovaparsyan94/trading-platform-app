from typing import List
from src.apps.trading_platform.models import DealSettings
from src.apps.trading_platform.repositories.i_deal_repository import IDealRepository


class DjangoORMDealRepository(IDealRepository):
    def get_deal_by_id(self, deal_id: int) -> DealSettings:
        """Fetch a deal from the database by its ID."""
        try:
            return DealSettings.objects.get(id=deal_id)
        except DealSettings.DoesNotExist:
            return None

    def get_all_deals(self) -> List[DealSettings]:
        """Fetch all deals from the database."""
        return list(DealSettings.objects.all())


def example_usage():
    deal_repository = DjangoORMDealRepository()
    all_deals = deal_repository.get_all_deals()
    print(f"All deals: {all_deals}")


example_usage()
from src.apps.trading_platform.models import DealSettings
from src.apps.trading_platform.repositories.i_deal_repository import IDealRepository


class DjangoORMDealRepository(IDealRepository):
    def get_deal_by_id_or_none(self, deal_id: int) -> DealSettings | None:
        """Fetch a deal from the database by its ID."""
        try:
            return DealSettings.objects.get(id=deal_id)
        except DealSettings.DoesNotExist:
            return None

    def get_all_deals(self) -> list[DealSettings]:
        """Fetch all deals from the database."""
        return list(DealSettings.objects.all())

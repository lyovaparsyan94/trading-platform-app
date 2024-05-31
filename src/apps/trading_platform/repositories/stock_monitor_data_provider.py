import json

from django.core.exceptions import ObjectDoesNotExist
from selenium.webdriver.ie.webdriver import WebDriver

from src.apps.trading_platform.interfaces.stock_data_repository import StockDataProvideRepository
from src.apps.trading_platform.models import StockMonitorConfiguration


class StockMonitorCookiesPayloadProvider(StockDataProvideRepository):
    def get_first_obj(self) -> dict:
        config = StockMonitorConfiguration.objects.first()
        if config is not None:
            return config.stockmonitor_cookies
        else:
            raise ValueError

    def get_payload(self, strategy_name: str) -> dict:
        config = StockMonitorConfiguration.objects.first()
        if config is None:
            raise NotImplementedError(f"Strategy '{strategy_name}' not implemented.")
        if strategy_name == 'long':
            return config.long_strategy_payload
        elif strategy_name == 'short':
            return config.short_strategy_payload

    def export_cookies(self, driver: WebDriver) -> None:
        cookies = driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        config = StockMonitorConfiguration.objects.first()
        if config is None:
            raise ValueError

        config.stockmonitor_cookies = cookies_dict
        config.save()

    def load_cookies(self) -> dict:
        config = StockMonitorConfiguration.objects.first()
        if config is not None:
            return config.stockmonitor_cookies
        else:
            raise ValueError

    def update_payload_to_first_obj(self, payload: str, strategy_name: str) -> None:
        config = StockMonitorConfiguration.objects.first()
        if config is None:
            raise ValueError

        if strategy_name == 'long':
            config.long_strategy_payload = json.loads(payload)
        elif strategy_name == 'short':
            config.short_strategy_payload = json.loads(payload)
        config.save()

    def load_credentials(self) -> tuple[str, str]:
        try:
            config = StockMonitorConfiguration.objects.first()
            if config is not None:
                return config.email, config.password
            else:
                raise ValueError
        except ObjectDoesNotExist:
            raise ValueError

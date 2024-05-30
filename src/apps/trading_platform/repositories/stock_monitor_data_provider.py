import json
from typing import Any

from selenium.webdriver.ie.webdriver import WebDriver

from src.apps.trading_platform.interfaces.i_stock_data_repository import IStockDataProvideRepository
from src.apps.trading_platform.models import StockMonitorConfiguration


class StockMonitorCookiesPayloadProvider(IStockDataProvideRepository):
    def get_cookies(self) -> dict | Any:
        config = StockMonitorConfiguration.objects.first()
        if config:
            return config.stockmonitor_cookies
        else:
            raise ValueError

    def get_payload(self, strategy_name: str) -> dict | Any:
        config = StockMonitorConfiguration.objects.first()
        if not config:
            raise ValueError

        if strategy_name == 'long':
            return config.long_strategy_payload
        elif strategy_name == 'short':
            return config.short_strategy_payload
        else:
            raise NotImplementedError(f"Strategy '{strategy_name}' not implemented.")

    def export_cookies(self, driver: WebDriver) -> None:
        cookies = driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        config = StockMonitorConfiguration.objects.first()
        if config:
            config.stockmonitor_cookies = cookies_dict
            config.save()
        else:
            raise ValueError

    def load_cookies(self) -> dict | Any:
        config = StockMonitorConfiguration.objects.first()
        if config:
            return config.stockmonitor_cookies
        else:
            raise ValueError

    def update_payload(self, payload: str, strategy_name: str) -> None:
        config = StockMonitorConfiguration.objects.first()
        if config:
            if strategy_name == 'long':
                config.long_strategy_payload = json.loads(payload)
            elif strategy_name == 'short':
                config.short_strategy_payload = json.loads(payload)
            config.save()
        else:
            raise ValueError

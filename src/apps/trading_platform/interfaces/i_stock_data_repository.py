from abc import ABC, abstractmethod
from typing import Any

from selenium.webdriver.ie.webdriver import WebDriver


class IStockDataProvideRepository(ABC):
    @abstractmethod
    def get_cookies(self) -> dict | Any:
        raise NotImplementedError

    @abstractmethod
    def get_payload(self, strategy_name: str) -> dict | Any:
        raise NotImplementedError

    @abstractmethod
    def export_cookies(self, driver: WebDriver) -> None:
        raise NotImplementedError

    def load_cookies(self) -> dict | Any:
        raise NotImplementedError

    @abstractmethod
    def update_payload(self, payload: str, strategy_name: str) -> None:
        raise NotImplementedError

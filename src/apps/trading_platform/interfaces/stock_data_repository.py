from abc import ABC, abstractmethod

from selenium.webdriver.ie.webdriver import WebDriver


class StockDataProvideRepository(ABC):
    @abstractmethod
    def get_first_obj(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_payload(self, strategy_name: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def export_cookies(self, driver: WebDriver) -> None:
        raise NotImplementedError

    def load_cookies(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_payload_to_first_obj(self, payload: str, strategy_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_credentials(self) -> tuple[str, str]:
        raise NotImplementedError

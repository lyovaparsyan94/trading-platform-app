from abc import ABC, abstractmethod


class DataScraper(ABC):
    @abstractmethod
    def scrape(self, stock_count: int, strategy_name: str, info: list[str]) -> list[str]:
        raise NotImplementedError

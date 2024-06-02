from abc import ABC, abstractmethod


class StocksScraper(ABC):
    @abstractmethod
    def scrape(self, stock_count: int, info: list[str]) -> list[str]:
        raise NotImplementedError

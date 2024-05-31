
from bs4 import BeautifulSoup

from src.apps.trading_platform.interfaces.data_scraper import DataScraper


class BeautifulSoupDataScraper(DataScraper):
    def scrape(self, stock_count: int, strategy_name: str, info: list[str]) -> list[str]:
        symbols = []
        for html in info:
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.select('a[href*="/charts/?s"]'):
                symbol = link.text
                symbols.append(symbol)
                if len(symbols) >= stock_count:
                    break
        return symbols

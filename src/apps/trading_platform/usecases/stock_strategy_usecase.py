import logging
import requests
from src.apps.trading_platform.adapters.bs4_data_scraper import BeautifulSoupStocksScraper
from src.apps.trading_platform.adapters.stock_monitor_data_updater import StockMonitorDataUpdater
from src.apps.trading_platform.adapters.stock_monitor_request_sender import StockMonitorRequestSender
from src.apps.trading_platform.adapters.urlpatterns import (
    STOCKMONITOR_TEST_RESULT_PAGE_URL,
    STOCKMONITOR_TEST_RESULT_URL,
    STOCKMONITOR_TEST_URL,
)
from src.apps.trading_platform.interfaces.base_stocks_strategy_use_case import BaseStocksStrategyUseCase
from src.apps.trading_platform.repositories.stock_monitor_data_provider import StockMonitorCookiesPayloadProvider

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelень)s - %(message)s')


class StockStrategyUseCase(BaseStocksStrategyUseCase):
    def __init__(self,
                 data_repository: StockMonitorCookiesPayloadProvider,
                 request_sender: StockMonitorRequestSender,
                 data_scraper: BeautifulSoupStocksScraper,
                 stockmonitor_authenticator: StockMonitorDataUpdater, strategy):
        self.strategy = strategy
        self.data_repository = data_repository
        self.request_sender = request_sender
        self.data_scraper = data_scraper
        self.stockmonitor_authenticator = stockmonitor_authenticator
        self._relogin()

    def get_stocks_for_strategy(self, stock_count: int, strategy_name: str) -> list[str]:
        strategy_sort = {'long': 'DESC', 'short': 'ASC'}
        config = self.data_repository.get_first_obj()
        cookies = config.stockmonitor_cookies

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,pl;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': ';'.join([f'{key}={value}' for key, value in cookies.items()]),
            'DNT': '1',
            'Origin': 'https://www.members.stockmonitor.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.members.stockmonitor.com/signal/?sid=86290',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/125.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }
        payload = config.long_strategy_payload if strategy_name == 'long' else config.short_strategy_payload
        first_request_data = payload
        first_response = self.request_sender.make_request(STOCKMONITOR_TEST_URL, headers=headers,
                                                          data=first_request_data)
        if first_response.status_code != 200:
            logger.info("Re-logging in due to failed first request")
            self._relogin()
        second_request_data = {"runId": payload['runId']}
        second_response = self.request_sender.make_request(STOCKMONITOR_TEST_RESULT_URL, headers=headers,
                                                           data=second_request_data)
        if second_response.status_code != 200:
            logger.info("Re-logging in due to failed second request")
            self._relogin()

        info = []
        page_count = stock_count // 12 if stock_count > 13 else 1
        for page in range(page_count):
            paged_request_data = {
                "runId": payload['runId'],
                "page": str(page + 1),
                "orderState": {
                    "field": "pchange",
                    "dir": strategy_sort[strategy_name]
                }
            }
            response = self.request_sender.make_request(STOCKMONITOR_TEST_RESULT_PAGE_URL, headers=headers,
                                                        data=paged_request_data)
            if response.status_code != 200 or not response.content:
                logger.info(f"Failed to get valid response or empty content for page {page + 1}")
                self._relogin()
                continue

            try:
                response_json = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from page {page + 1} response: {e}")
                self._relogin()
                continue

            info.append(response_json.get('html', ''))

        trade_symbols = self.data_scraper.scrape(stock_count=stock_count, info=info)
        logger.info(trade_symbols)
        return trade_symbols

    def _relogin(self) -> None:
        logger.info("Re-logging in to update data...")
        logger.info("getting long strategy payload...")
        self.stockmonitor_authenticator.update_data(self.strategy)

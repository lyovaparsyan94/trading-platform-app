import logging

from src.apps.trading_platform.adapters.bs4_data_scraper import BeautifulSoupDataScraper
from src.apps.trading_platform.adapters.stock_monitor_data_updater import StockMonitorDataUpdater
from src.apps.trading_platform.adapters.stock_monitor_request_sender import StockMonitorRequestSender
from src.apps.trading_platform.adapters.urlpatterns import (
    STOCKMONITOR_TEST_RESULT_PAGE_URL,
    STOCKMONITOR_TEST_RESULT_URL,
    STOCKMONITOR_TEST_URL,
)
from src.apps.trading_platform.repositories.stock_monitor_data_provider import StockMonitorCookiesPayloadProvider

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class StockStrategyUsecase:
    def __init__(self,
                 data_repository: StockMonitorCookiesPayloadProvider,
                 request_sender: StockMonitorRequestSender,
                 data_scraper: BeautifulSoupDataScraper,
                 stockmonitor_authenticator: StockMonitorDataUpdater):
        self.data_repository = data_repository
        self.request_sender = request_sender
        self.data_scraper = data_scraper
        self.stockmonitor_authenticator = stockmonitor_authenticator

    def get_stocks_for_strategy(self, stock_count: int, strategy_name: str) -> list[str]:
        strategy_sort = {'long': 'DESC', 'short': 'ASC'}
        cookies = self.data_repository.get_first_obj()
        headers = self.request_sender.get_headers(cookies=cookies)
        payload = self.data_repository.get_payload(strategy_name=strategy_name)

        first_response = self.request_sender.first_request(STOCKMONITOR_TEST_URL, payload=payload, headers=headers)
        if first_response.status_code != 200:
            logger.info("Re-logging in due to failed first request")
            self.relogin()

        second_response = self.request_sender.second_request(STOCKMONITOR_TEST_RESULT_URL,
                                                             payload={'runId': payload['runId']}, headers=headers)
        if second_response.status_code != 200:
            logger.info("Re-logging in due to failed second request")
            self.relogin()

        info = self.request_sender.make_request(STOCKMONITOR_TEST_RESULT_PAGE_URL, stock_count=stock_count,
                                                headers=headers, payload=payload,
                                                dir_=strategy_sort[strategy_name])
        trade_symbols = self.data_scraper.scrape(stock_count=stock_count, strategy_name=strategy_name, info=info)
        logger.info(trade_symbols)
        return trade_symbols

    def relogin(self) -> None:
        self.stockmonitor_authenticator.update_data()
        logger.info("Re-logging in to update data...")

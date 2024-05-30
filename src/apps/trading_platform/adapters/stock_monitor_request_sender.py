import logging

import requests
from bs4 import BeautifulSoup

from src.apps.trading_platform.adapters.stock_monitor_data_updater import StockMonitorDataUpdater
from src.apps.trading_platform.adapters.urlpatterns import (
    STOCKMONITOR_TEST_RESULT_PAGE_URL,
    STOCKMONITOR_TEST_RESULT_URL,
    STOCKMONITOR_TEST_URL,
)
from src.apps.trading_platform.repositories.stock_monitor_data_provider import StockMonitorCookiesPayloadProvider

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class StockMonitorRequestSender:

    def __init__(self, data_repository_instance: StockMonitorCookiesPayloadProvider):
        self.data_repository = data_repository_instance()

    def relogin(self):
        # not defined in init, as not to  initialize webdriver, if not necessary
        self.stockmonitor_authenticator = StockMonitorDataUpdater(
            data_repository_instance=self.data_repository_instance)

    def get_headers(self, cookies):
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
        return headers

    def first_request(self, payload, headers):
        url = STOCKMONITOR_TEST_URL
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            logger.info(f"first request: {response.status_code}, need login")
            self.relogin()
        return response.status_code

    def second_request(self, payload, headers):
        url = STOCKMONITOR_TEST_RESULT_URL
        data = {"runId": payload['runId']}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            logger.info(f"second request {response.status_code}, need login")
            self.relogin()
        return response

    def get_stocks_for_strategy(self, stock_count, strategy_name):
        strategy_sort = {'long': 'DESC', 'short': 'ASC'}
        cookies = self.data_repository.get_cookies()
        headers = self.get_headers(cookies=cookies)
        payload = self.data_repository.get_payload(strategy_name=strategy_name)

        self.first_request(payload=payload, headers=headers)
        self.second_request(payload=payload, headers=headers)

        info = self.make_request(stock_count=stock_count, headers=headers, payload=payload,
                                 dir_=strategy_sort[strategy_name])
        trade_symbols = self.scrape(stock_count=stock_count, strategy_name=strategy_name, info=info)
        logger.info(trade_symbols)
        return trade_symbols

    def make_request(self, stock_count, headers, payload, dir_="DESC", ):
        info = []

        page_count = stock_count // 12 if stock_count > 13 else 1
        for page in range(page_count):
            url = STOCKMONITOR_TEST_RESULT_PAGE_URL
            data = {
                "runId": payload['runId'],
                "page": str(page + 1),
                "orderState": {
                    "field": "pchange",
                    "dir": dir_
                }
            }
            response = requests.post(url, headers=headers, json=data)
            info.append(response.json().get('html', ''))
        return info

    def scrape(self, stock_count, strategy_name, info: list):
        symbols = []
        for html in info:
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.select('a[href*="/charts/?s"]'):
                symbol = link.text
                symbols.append(symbol)
                if len(symbols) >= stock_count:
                    break
        logger.info(f"get {len(symbols)} stocks for {strategy_name} trading")
        return symbols




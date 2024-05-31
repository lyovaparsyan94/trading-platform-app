import logging

import requests

from src.apps.trading_platform.adapters.bs4_data_scraper import BeautifulSoupDataScraper
from src.apps.trading_platform.interfaces.request_sender import RequestSender
from src.apps.trading_platform.repositories.stock_monitor_data_provider import StockMonitorCookiesPayloadProvider

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class StockMonitorRequestSender(RequestSender):
    def __init__(self,
                 data_repository_instance: StockMonitorCookiesPayloadProvider,
                 data_scraper: BeautifulSoupDataScraper,
                 ) -> None:
        self.data_repository = data_repository_instance
        self.data_scraper = data_scraper

    def get_headers(self, cookies: dict[str, str]) -> dict[str, str]:
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

    def first_request(self, url: str, payload: dict, headers: dict[str, str]) -> requests.Response:
        response = requests.post(url, headers=headers, json=payload)
        return response

    def second_request(self, url: str, payload: dict, headers: dict[str, str]) -> requests.Response:
        data = {"runId": payload['runId']}
        response = requests.post(url, headers=headers, json=data)
        return response

    def make_request(self, url: str, stock_count: int, headers: dict[str, str], payload: dict, dir_: str) -> list[str]:
        info = []
        page_count = stock_count // 12 if stock_count > 13 else 1
        for page in range(page_count):
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

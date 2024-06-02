import logging

import requests

from src.apps.trading_platform.interfaces.request_sender import RequestSender

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class StockMonitorRequestSender(RequestSender):
    def make_request(self, url: str, headers: dict[str, str], data: dict) -> requests.Response:
        response = requests.post(url, headers=headers, json=data)
        return response

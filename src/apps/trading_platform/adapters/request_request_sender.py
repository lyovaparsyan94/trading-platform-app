import requests

from src.apps.trading_platform.adapters.urlpatterns import STOCKMONITOR_TEST_RESULT_URL, STOCKMONITOR_TEST_URL
from src.apps.trading_platform.interfaces.request_sender import RequestSender


class RequestSender(RequestSender):
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

    def send_request(self, url: str, payload: dict, headers: dict[str, str]) -> requests.Response:
        response = requests.post(url, headers=headers, json=payload)
        return response

    def first_request(self, payload: dict, headers: dict[str, str]) -> requests.Response:
        url = STOCKMONITOR_TEST_URL
        response = requests.post(url, headers=headers, json=payload)
        return response

    def second_request(self, payload: dict, headers: dict[str, str]) -> requests.Response:
        url = STOCKMONITOR_TEST_RESULT_URL
        data = {"runId": payload['runId']}
        response = requests.post(url, headers=headers, json=data)
        return response

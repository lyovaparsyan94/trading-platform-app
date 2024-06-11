import json
import requests
from bs4 import BeautifulSoup


class StockMonitorFetcher:
    def __init__(self, cookie_handler):
        self.cookie_handler = cookie_handler
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,pl;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'DNT': '1',
            'Origin': 'https://www.members.stockmonitor.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.members.stockmonitor.com/signal/?sid=86290',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }

    def update_headers_with_cookies(self):
        cookies = self.cookie_handler.ensure_valid_cookies()
        self.headers['Cookie'] = '; '.join([f'{key}={value}' for key, value in cookies.items()])

    def perform_initial_requests(self):
        url_first_curl = 'https://www.members.stockmonitor.com/signal/test/'
        response_first = requests.post(url_first_curl, headers=self.headers, data=json.dumps(payload_first_curl))
        print(f"First response: {response_first.text}")

        response_first_data = response_first.json()
        self.run_id = response_first_data.get('runId', payload_first_curl["runId"])

        url_second_curl = 'https://www.members.stockmonitor.com/signal/test-result'
        payload_second_curl = {
            "runId": self.run_id
        }
        response_second = requests.post(url_second_curl, headers=self.headers, data=json.dumps(payload_second_curl))
        print(f"Second response: {response_second.text}")

    def make_third_request(self, symbol_count, sort='ASC'):
        url_third_curl = 'https://www.members.stockmonitor.com/signal/test-result-page'
        symbols = []
        page = 1

        while len(symbols) < symbol_count:
            payload_third_curl = {
                "runId": self.run_id,
                "page": str(page),
                "orderState": {
                    "field": "pchange",
                    "dir": sort
                }
            }
            response_third = requests.post(url_third_curl, headers=self.headers, data=json.dumps(payload_third_curl))
            print(f"Third response page {page}: {response_third.text}")

            if response_third.status_code == 200:
                response_data = response_third.json()
                html_content = response_data.get('html', '')
                soup = BeautifulSoup(html_content, 'html.parser')

                for link in soup.select('a[href*="/charts/?s"]'):
                    symbol = link.text
                    symbols.append(symbol)
                    if len(symbols) >= symbol_count:
                        break

            page += 1

        print(f"Extracted symbols: {symbols[:symbol_count]}, len: {len(symbols)}")

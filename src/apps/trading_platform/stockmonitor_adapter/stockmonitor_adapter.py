import requests
import json
from bs4 import BeautifulSoup


payload_first_curl = {
    "signalDef": {
        "grouping": "",
        "conds": [
            {
                "exprLeftItems": [
                    {
                        "bracketsOpen": "",
                        "runon": "daily",
                        "instrType": "barvalue",
                        "instrCode": "high",
                        "params": [],
                        "output": "-3:-1",
                        "bracketsClose": "",
                        "operator": "",
                        "value": ""
                    }
                ],
                "op": "decreasing",
                "exprRightItems": [
                    {
                        "bracketsOpen": "",
                        "runon": "daily",
                        "instrType": "barvalue",
                        "instrCode": "open",
                        "params": [],
                        "output": "0",
                        "bracketsClose": "",
                        "operator": ""
                    }
                ]
            }
        ]
    },
    "symbolsSet": "us-all",
    "timeframe": "daily",
    "candleOffset": "0",
    "is_snippet": False,
    "runId": "test-signal-1716908765750"
}

# Define headers
headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,pl;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': '_ga=GA1.2.1926989180.1715172452; _fbp=fb.1.1716403924871.1621444179; _gid=GA1.2.1757829315.1716815404; conv_source=; smsid=s%3AUIG2jEe-8DKuJw7eOvx9DXxeqAgxB_6R.vel2NbnEDqdIeMe5XkL25OTgBPpa2Ar7QkxaU3fotR8; _ga_5RGTB8Z129=GS1.2.1716908765.9.1.1716908766.0.0.0',
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

# Step 1: Send the first curl request
url_first_curl = 'https://www.members.stockmonitor.com/signal/test/'
response_first = requests.post(url_first_curl, headers=headers, data=json.dumps(payload_first_curl))
print(f"First response: {response_first.text}")

# Step 2: Send the second curl request
url_second_curl = 'https://www.members.stockmonitor.com/signal/test-result'
payload_second_curl = {
    "runId": "test-signal-1716908765750"
}
response_second = requests.post(url_second_curl, headers=headers, data=json.dumps(payload_second_curl))
# print(f"Second response: {response_second.text}")

# Step 3: Send the third curl request
url_third_curl = 'https://www.members.stockmonitor.com/signal/test-result-page'
payload_third_curl = {
    "runId": "test-signal-1716908765750",
    "page": "1",
    "orderState": {
        "field": "pchange",
        "dir": "DESC"
    }
}
response_third = requests.post(url_third_curl, headers=headers, data=json.dumps(payload_third_curl))
print(f"Third response: {response_third.text}")

symbols = []
if response_third.status_code == 200:
    response_data = response_third.json()
    html_content = response_data.get('html', '')
    soup = BeautifulSoup(html_content, 'html.parser')

    for link in soup.select('a[href*="/charts/?s"]'):
        symbol = link.text
        symbols.append(symbol)

print("Extracted symbols:", symbols)
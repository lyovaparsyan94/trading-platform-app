from urllib.parse import urlencode

from src.core.ioc import container

base_url = "https://signin.tradestation.com/authorize"


base_url = "https://signin.tradestation.com/authorize"
params = {
    "response_type": "code",
    "client_id": "lMujDTbmHrqZ5a7EkPSyskivY9doHu54",
    "redirect_uri": 'https://trading-platfrom.tw1.su/callback/',
    "audience": "https://api.tradestation.com",
    "scope": "openid offline_access profile MarketData ReadAccount Trade",
    "state": "STATE"
}
print(params)
url = f"{base_url}?{urlencode(params)}"
print(url)

# client_id = 'lMujDTbmHrqZ5a7EkPSyskivY9doHu54'
# client_secret = 'AIK6Sot-Nz_QbwbOUuL5TuYZx741S978Jnie3pRQUt7PwusNBA4KdbcV8epUdRzg'
# code = 'esn9syQVht9oJVbs'
# redirect_uri = 'https://trading-platfrom.tw1.su/callback/'

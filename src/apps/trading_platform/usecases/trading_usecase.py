import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings')
django.setup()

import requests

from src.apps.trading_platform.usecases.settings_trading_usecase import get_long_strategy_settings, get_short_strategy_settings, \
    get_long_stocks_for_strategy, get_short_stocks_for_strategy

base_url = "https://sim-api.tradestation.com/v3/"

token = ''  # replace with actual token


class Trader:
    def __init__(self, token=''):
        self.account_key = 'SIM2731552M'
        self.check_token()
        self.account_name = "my_trading_strategies"
        self.long_strategy_settings = get_long_strategy_settings(self.account_name)
        self.short_strategy_settings = get_short_strategy_settings(self.account_name)
        print('short_strategy_settings', self.short_strategy_settings, )
        print("=" * 30)
        print('long_strategy_settings', self.long_strategy_settings, )
        self.top_long_stocks = get_long_stocks_for_strategy(self.account_name)
        self.top_short_stocks = get_short_stocks_for_strategy(self.account_name)

        self.token = token
        self.buy_or_sell = {'long': 'BUY', 'short': 'SELL'}

    def check_token(self):
        headers = {
            'Authorization': f'Bearer {token}',
        }

        response = requests.get(f'https://api.tradestation.com/v3/brokerage/accounts', headers=headers)
        if response.json().get('Message') or response.status_code < response.ok:
            print(response.json())
        if response.status_code == 200:
            print('token is valid', response.status_code)

    def get_account_id(self, token):
        headers = {
            'Authorization': f'Bearer {token}',
        }

        response = requests.get(f'https://api.tradestation.com/v3/brokerage/accounts', headers=headers)
        if response.json():
            print('Account ID: ', response.json()['Accounts'][0]['AccountID'])
        return response.json()['Accounts'][0]['AccountID']

    def get_balance(self, token, account_key):
        headers = {
            'Authorization': f'Bearer  {token}',
        }

        response = requests.get(f'{base_url}accounts/{account_key}/balances', headers=headers)
        print(response.json())

    def confirm_order(self, symbol, strategy_name):
        url = f"{base_url}orderexecution/orderconfirm"

        payload = {
            "AccountID": self.get_account_id(self.token),
            "Symbol": symbol,
            "Quantity": "1",
            "OrderType": "Market",
            "TradeAction": self.buy_or_sell[strategy_name],
            "TimeInForce": {"Duration": "DAY"},
            "Route": "Intelligent"
        }
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

    def cancel_order(self, token):
        url = f"{base_url}orderexecution/orders/123456789"

        headers = {"Authorization": f"Bearer {token}"}

        response = requests.request("DELETE", url, headers=headers)

        print(response.text)

    def place_order(self, symbol, quantity, strategy_name):
        # account_id = self.get_account_id(token)
        if strategy_name.lower() == 'long':
            stop_loss_percent = self.long_strategy_settings['stop_loss_percentage_long']
            take_profit_percent = self.long_strategy_settings['take_profit_percentage_long_time_1']
        elif strategy_name.lower() == 'short':
            stop_loss_percent = self.short_strategy_settings['stop_loss_percentage_short']
            take_profit_percent = self.short_strategy_settings['take_profit_percentage_short_time_1']
        else:
            raise NotImplementedError

        symbol_price = self.get_symbol_price(symbol, strategy_name)
        stop_loss_price = symbol_price - (symbol_price * stop_loss_percent / 100)
        take_profit_price = symbol_price + (symbol_price * take_profit_percent / 100)

        url = f"{base_url}orderexecution/orders"

        payload = {
            "AccountID": "SIM2731552M",
            "Symbol": str(symbol),
            "Quantity": str(quantity),
            "OrderType": "Limit",
            "LimitPrice": str(take_profit_price),
            "StopPrice": str(stop_loss_price),
            "TradeAction": self.buy_or_sell[strategy_name],
            "TimeInForce": {
                "Duration": "DAY"
            },
            "Route": "Intelligent"
        }

        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        print(url)
        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

    def get_symbol_price(self, symbol, strategy_name):
        if strategy_name.lower() == 'long':
            price_type = 'Ask'
        elif strategy_name.lower() == 'short':
            price_type = 'Bid'
        else:
            raise NotImplementedError
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        response = requests.get(f'{base_url}/data/quote/{symbol}', headers=headers)
        if response.status_code != 200:
            raise NotImplementedError
        print(
            f"Stock {symbol}'s Ask - {response.json()[0]['Ask']}, 'Bid' - {response.json()[0]['Bid']}, for {strategy_name} strategy  use {response.json()[0][price_type]}")

        return response.json()[0][price_type]


trader = Trader(token)
trader.place_order(quantity="10", symbol='AMZN', strategy_name='long')

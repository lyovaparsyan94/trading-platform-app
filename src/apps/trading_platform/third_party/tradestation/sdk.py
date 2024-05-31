from abc import ABC, abstractmethod

from src.apps.trading_platform.third_party.tradestation.client import TradeStationHTTPClient
from src.apps.trading_platform.third_party.tradestation.schemas.exchange_code_to_tokens import \
    ExchangeCodeToTokensOutput
from src.apps.trading_platform.third_party.tradestation.urlpatterns import TRADESTATION_SIGN_IN_EXCHANGE_TOKEN_URL


class BaseTradeStationSDK(ABC):

    def __init__(
        self,
        client: TradeStationHTTPClient,
    ):
        self.client = client

    @abstractmethod
    def exchange_code_to_tokens(
        self,
        client_id: str,
        client_secret: str,
        code: str,
        redirect_uri: str,
        grant_type: str = "authorization_code",
    ) -> ExchangeCodeToTokensOutput:
        raise NotImplementedError


class TradeStationSDK(BaseTradeStationSDK):

    def exchange_code_to_tokens(self, client_id: str, client_secret: str, code: str, redirect_uri: str,
                                grant_type: str = "authorization_code") -> ExchangeCodeToTokensOutput:
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri,
        }
        response_json = self.client.request(
            method="POST",
            url=TRADESTATION_SIGN_IN_EXCHANGE_TOKEN_URL,
            headers=headers,
            data=data,
        )
        return ExchangeCodeToTokensOutput(
            **response_json
        )

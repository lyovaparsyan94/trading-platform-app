from dependency_injector import containers, providers

from src.apps.trading_platform.adapters.access_trade_provider import AccessTradeProvider
from src.apps.trading_platform.third_party.tradestation.client import TradeStationHTTPClient, \
    RequestsTradeStationHTTPClient
from src.apps.trading_platform.third_party.tradestation.sdk import TradeStationSDK


class Container(containers.DeclarativeContainer):
    access_trade_provider = providers.Singleton(
        AccessTradeProvider
    )
    tradestation_requests_client = providers.Singleton(
        RequestsTradeStationHTTPClient,
        proxy=None,
    )
    tradestation_sdk = providers.Singleton(
        TradeStationSDK,
        client=tradestation_requests_client,
    )


container = Container()

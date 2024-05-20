from dependency_injector import containers, providers

from src.apps.trading_platform.adapters.access_trade_provider import AccessTradeProvider


class Container(containers.DeclarativeContainer):
    access_trade_provider = providers.Singleton(
        AccessTradeProvider
    )


container = Container()


from .stock_strategy_usecase import StockStrategyUseCase
from ..adapters.bs4_data_scraper import BeautifulSoupStocksScraper
from ..adapters.element_handler import ElementHandler
from ..adapters.stock_monitor_data_updater import BaseDriver, StockMonitorDataUpdater
from ..adapters.stock_monitor_request_sender import StockMonitorRequestSender
from ..models import TradingAccount, DealSettings
from ..repositories.stock_monitor_data_provider import StockMonitorCookiesPayloadProvider


def get_long_strategy_settings(account_name):
    try:
        trading_account = TradingAccount.objects.get(name=account_name)
    except TradingAccount.DoesNotExist:
        raise ValueError("Trading Account not found")

    try:
        deal_settings = DealSettings.objects.get(trading_account=trading_account)
    except DealSettings.DoesNotExist:
        raise ValueError("DealSettings not found for the given Trading Account")

    long_strategy_settings = {
        "enable_long_strategy": deal_settings.enable_long_strategy,
        "stop_loss_percentage_long": deal_settings.stop_loss_percentage_long,
        "top_stocks_long": deal_settings.top_stocks_long,
        "take_profit_percentage_long_time_1": deal_settings.take_profit_percentage_long_time_1,
        "take_profit_percentage_long_1": deal_settings.take_profit_percentage_long_1,
        "take_profit_percentage_long_time_2": deal_settings.take_profit_percentage_long_time_2,
        "take_profit_percentage_long_2": deal_settings.take_profit_percentage_long_2,
        "take_profit_percentage_long_time_3": deal_settings.take_profit_percentage_long_time_3,
        "take_profit_percentage_long_3": deal_settings.take_profit_percentage_long_3,
        "take_profit_percentage_long_time_4": deal_settings.take_profit_percentage_long_time_4,
        "take_profit_percentage_long_4": deal_settings.take_profit_percentage_long_4,
        "take_profit_percentage_long_time_5": deal_settings.take_profit_percentage_long_time_5,
        "take_profit_percentage_long_5": deal_settings.take_profit_percentage_long_5,
    }
    return long_strategy_settings


def get_short_strategy_settings(account_name):
    try:
        trading_account = TradingAccount.objects.get(name=account_name)
    except TradingAccount.DoesNotExist:
        raise ValueError("Trading Account not found")

    try:
        deal_settings = DealSettings.objects.get(trading_account=trading_account)
    except DealSettings.DoesNotExist:
        raise ValueError("DealSettings not found for the given Trading Account")

    short_strategy_settings = {
        "enable_short_strategy": deal_settings.enable_short_strategy,
        "stop_loss_percentage_short": deal_settings.stop_loss_percentage_short,
        "top_stocks_short": deal_settings.top_stocks_short,
        "take_profit_percentage_short_time_1": deal_settings.take_profit_percentage_short_time_1,
        "take_profit_percentage_short_1": deal_settings.take_profit_percentage_short_1,
        "take_profit_percentage_short_time_2": deal_settings.take_profit_percentage_short_time_2,
        "take_profit_percentage_short_2": deal_settings.take_profit_percentage_short_2,
        "take_profit_percentage_short_time_3": deal_settings.take_profit_percentage_short_time_3,
        "take_profit_percentage_short_3": deal_settings.take_profit_percentage_short_3,
        "take_profit_percentage_short_time_4": deal_settings.take_profit_percentage_short_time_4,
        "take_profit_percentage_short_4": deal_settings.take_profit_percentage_short_4,
        "take_profit_percentage_short_time_5": deal_settings.take_profit_percentage_short_time_5,
        "take_profit_percentage_short_5": deal_settings.take_profit_percentage_short_5,
    }
    return short_strategy_settings


def get_long_stocks_for_strategy(account_name):
    try:
        long_strategy_settings = get_long_strategy_settings(account_name)

        if not long_strategy_settings["enable_long_strategy"]:
            raise ValueError("Long Strategy is not enabled for this account")

        top_stocks_long = long_strategy_settings["top_stocks_long"]
        if top_stocks_long is None:
            raise ValueError("Top Stocks for Long Strategy is not set")

        driver = BaseDriver(headless_mode=True).get_driver()
        element_handler = ElementHandler(driver)
        data_repository = StockMonitorCookiesPayloadProvider()
        data_scraper = BeautifulSoupStocksScraper()
        request_sender = StockMonitorRequestSender()
        stockmonitor_long_authenticator = StockMonitorDataUpdater(data_repository_instance=data_repository,
                                                                  element_handler=element_handler, driver=driver)

        usecase = StockStrategyUseCase(data_repository, request_sender, data_scraper, stockmonitor_long_authenticator,
                                       strategy='long')
        long_stocks = usecase.get_stocks_for_strategy(stock_count=top_stocks_long, strategy_name='long')
        return long_stocks

    except ValueError as e:
        print(f"Error: {e}")
        return None


def get_short_stocks_for_strategy(account_name):
    try:
        short_strategy_settings = get_short_strategy_settings(account_name)

        if not short_strategy_settings["enable_short_strategy"]:
            raise ValueError("Short Strategy is not enabled for this account")

        top_stocks_short = short_strategy_settings["top_stocks_short"]
        if top_stocks_short is None:
            raise ValueError("Top Stocks for Short Strategy is not set")

        driver = BaseDriver(headless_mode=True).get_driver()
        element_handler = ElementHandler(driver)
        data_repository = StockMonitorCookiesPayloadProvider()
        data_scraper = BeautifulSoupStocksScraper()
        request_sender = StockMonitorRequestSender()
        stockmonitor_long_authenticator = StockMonitorDataUpdater(data_repository_instance=data_repository,
                                                                  element_handler=element_handler, driver=driver)

        usecase = StockStrategyUseCase(data_repository, request_sender, data_scraper, stockmonitor_long_authenticator,
                                       strategy='short')

        short_stocks = usecase.get_stocks_for_strategy(stock_count=top_stocks_short, strategy_name='short')
        return short_stocks

    except ValueError as e:
        print(f"Error: {e}")
        return None

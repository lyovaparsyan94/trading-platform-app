import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings')
django.setup()

from src.apps.trading_platform.adapters.bs4_data_scraper import BeautifulSoupDataScraper
from src.apps.trading_platform.adapters.element_handler import ElementHandler
from src.apps.trading_platform.adapters.stock_monitor_data_updater import BaseDriver, StockMonitorDataUpdater
from src.apps.trading_platform.adapters.stock_monitor_request_sender import StockMonitorRequestSender
from src.apps.trading_platform.adapters.stock_strategy_usecase import StockStrategyUsecase
from src.apps.trading_platform.repositories.stock_monitor_data_provider import StockMonitorCookiesPayloadProvider

driver = BaseDriver(headless_mode=True).get_driver()
element_handler = ElementHandler(driver)
data_repository = StockMonitorCookiesPayloadProvider()
data_scraper = BeautifulSoupDataScraper()
request_sender = StockMonitorRequestSender(data_repository_instance=data_repository, data_scraper=data_scraper, )
stockmonitor_authenticator = StockMonitorDataUpdater(data_repository_instance=data_repository,
                                                     element_handler=element_handler, driver=driver, )
usecase = StockStrategyUsecase(data_repository, request_sender, data_scraper, stockmonitor_authenticator, )

# stocks = usecase.get_stocks_for_strategy(stock_count=12, strategy_name='long')
# print(len(stocks))
stocks1 = usecase.get_stocks_for_strategy(stock_count=12, strategy_name='short', )
print(len(stocks1))
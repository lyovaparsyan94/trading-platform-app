from src.apps.trading_platform.stockmonitor_adapter.cookie_handler import CookieHandler
from src.apps.trading_platform.stockmonitor_adapter.stock_monitor_fetcher import StockMonitorFetcher

email = "bassam19789000@gmail.com"
password = "Alkhulaifib@504"

cookie_handler = CookieHandler(email, password)
stock_monitor_fetcher = StockMonitorFetcher(cookie_handler)

# Обновление заголовков с куки
stock_monitor_fetcher.update_headers_with_cookies()

# Выполнение начальных запросов
stock_monitor_fetcher.perform_initial_requests()

# Выполнение третьего запроса с указанием необходимого количества символов
stock_monitor_fetcher.make_third_request(symbol_count=12, sort='DESC')

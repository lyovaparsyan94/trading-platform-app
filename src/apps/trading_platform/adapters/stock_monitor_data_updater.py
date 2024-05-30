import time

from django.core.exceptions import ObjectDoesNotExist
from seleniumwire import webdriver

from src.apps.trading_platform.adapters.element_handler import ElementHandler
from src.apps.trading_platform.adapters.urlpatterns import STOCKMONITOR_BASE_URL, STOCKMONITOR_FILTERS_PAGE_URL
from src.apps.trading_platform.models import StockMonitorConfiguration
from src.apps.trading_platform.repositories.stock_monitor_data_provider import StockMonitorCookiesPayloadProvider


class BaseDriver:
    def __init__(self, headless_mode: bool) -> None:
        self.options = webdriver.ChromeOptions()
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        self.options.add_experimental_option("prefs", prefs)
        if headless_mode:
            self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)


class StockMonitorDataUpdater:

    def __init__(self,
                 data_repository_instance: StockMonitorCookiesPayloadProvider,
                 element_handler: ElementHandler = ElementHandler,
                 headless_mode=False,
                 ) -> None:
        self.data_repository = data_repository_instance()
        self.headless_mode = headless_mode
        self.driver = BaseDriver(headless_mode=headless_mode).driver
        self.element_handler = element_handler(driver=self.driver)
        self.base_url: str = STOCKMONITOR_BASE_URL
        self.filters_page_url: str = STOCKMONITOR_FILTERS_PAGE_URL
        self.email = None
        self.password = None
        self.load_credentials()

    def load_credentials(self):
        try:
            config = StockMonitorConfiguration.objects.first()
            if config:
                self.email = config.email
                self.password = config.password
            else:
                raise ValueError("Configuration not found in the database.")
        except ObjectDoesNotExist:
            raise ValueError("Configuration not found in the database.")

    def open_stockmonitor_page(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(self.base_url)

    def login(self) -> None:
        incorrect_input = True
        while incorrect_input:
            email_field = self.element_handler.wait_for_element(locator='//*[@id="email"]', name='email field')
            email_field.clear()
            self.element_handler.slow_input(email_field, self.email)
            password_field = self.element_handler.wait_for_element(locator='//*[@id="pwd"]', name='password field')
            password_field.clear()
            self.element_handler.slow_input(password_field, self.password)
            login_button = self.element_handler.wait_for_element(locator='//*[@id="btn-send"]', name='login button')
            login_button.click()
            incorrect_input = self.element_handler.is_shown_warning(
                warning_xpath='//*[@id="errors"]', name='incorrect input')

    def go_filter_pages(self) -> None:
        self.data_repository.export_cookies(driver=self.driver)

        self.driver.get(self.filters_page_url)
        while "stockmonitor.com/signals/" not in self.driver.current_url:
            time.sleep(1)
            self.driver.get(self.filters_page_url)
        long_page = self.element_handler.wait_for_element(
            locator="//*[@id='table-signals']//a[contains(text(),'LONG')]", name='Sample Filter')
        long_page_href = long_page.get_attribute('href')
        short_page = self.element_handler.wait_for_element(
            locator="//*[@id='table-signals']//a[contains(text(),'SHORT')]", name='Sample Filter')
        short_page_href = short_page.get_attribute('href')
        strategies = {'long': [long_page, long_page_href], 'short': [short_page, short_page_href]}
        for strategy_name, strategy in strategies.items():
            if strategy:
                self.driver.get(strategy[-1])
                test_filter = self.element_handler.wait_for_element(
                    locator='//*[@id="btn-test"]', name='test filter')
                if test_filter:
                    test_filter.click()
                    request = self.driver.wait_for_request('https://www.members.stockmonitor.com/signal/test/')
                    self.intercept_requests(request=request, strategy_name=strategy_name)

    def intercept_requests(self, request, strategy_name):
        time.sleep(2)
        if request.body:
            payload = request.body.decode('utf-8', errors='ignore')
            self.data_repository.update_payload(payload, strategy_name)

    def run(self) -> None:
        self.open_stockmonitor_page()
        self.login()
        self.go_filter_pages()
        self.driver.quit()

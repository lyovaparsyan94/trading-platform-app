import logging
import time

from requests import Request
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from src.apps.trading_platform.adapters.element_handler import ElementHandler
from src.apps.trading_platform.adapters.urlpatterns import (
    STOCKMONITOR_BASE_URL,
    STOCKMONITOR_FILTERS_PAGE_URL,
    STOCKMONITOR_TEST_URL,
)
from src.apps.trading_platform.interfaces.i_stock_monitor_data_updater import IStockMonitorDataUpdater
from src.apps.trading_platform.repositories.stock_monitor_data_provider import StockMonitorCookiesPayloadProvider

logger = logging.getLogger('element_handler')


class BaseDriver:
    def __init__(self, headless_mode: bool) -> None:
        self.disable_logs()
        self.options = webdriver.ChromeOptions()
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        self.options.add_experimental_option("prefs", prefs)
        if headless_mode:
            self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)

    def get_driver(self):
        return self.driver

    def disable_logs(self) -> None:
        seleniumwire_loggers = [
            'seleniumwire',
            'seleniumwire.storage',
            'seleniumwire.handler',
            'seleniumwire.backend'
        ]
        for logger_name in seleniumwire_loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.WARNING)


class StockMonitorDataUpdater(IStockMonitorDataUpdater):
    def __init__(self,
                 data_repository_instance: StockMonitorCookiesPayloadProvider,
                 element_handler: ElementHandler,
                 driver: WebDriver,
                 ) -> None:
        self.driver = driver
        self.data_repository = data_repository_instance
        self.element_handler = element_handler
        self.email = None
        self.password = None

    def get_email_password(self) -> None:
        config = self.data_repository.get_first_obj()
        self.email, self.password = config.email, config.password

    def open_stockmonitor_page(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(STOCKMONITOR_BASE_URL)

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

    def go_filter_page(self, strategy_name: str) -> None:
        self.data_repository.export_cookies(driver=self.driver)

        max_attempts = 10
        for attempt in range(max_attempts):
            self.driver.get(STOCKMONITOR_FILTERS_PAGE_URL)
            if "stockmonitor.com/signals/" in self.driver.current_url:
                break
            time.sleep(1)
        else:
            raise TimeoutError("Unable to load the filters page after multiple attempts.")

        page = self.element_handler.wait_for_element(
            locator=f"//*[@id='table-signals']//a[contains(text(),'{strategy_name.upper()}')]",
            name=f'{strategy_name} Filter')
        page_href = page.get_attribute('href')

        logger.info(f"Processing {strategy_name} strategy")
        logger.info(f"Navigating to URL: {page_href}")

        self.driver.get(page_href)

        common_stocks_button = self.element_handler.wait_for_element(locator='//*[@id="ssymbols-set"]',
                                                                     name='common_stocks')
        common_stocks_button.click()
        logger.info(f"Common stocks button clicked for {strategy_name} strategy")

        common_stocks_select = self.driver.find_element(By.XPATH, "//li[@data-value='us-type-stock']")
        common_stocks_select.click()
        logger.info(f"Common stocks select clicked for {strategy_name} strategy")

        test_filter = self.element_handler.wait_for_element(locator='//*[@id="btn-test"]', name='test filter')
        if test_filter:
            test_filter.click()
            logger.info(f"Test filter clicked for {strategy_name} strategy")
            request = self.driver.wait_for_request(STOCKMONITOR_TEST_URL)
            self.intercept_requests(request=request, strategy_name=strategy_name)

    def intercept_requests(self, request: Request, strategy_name: str) -> None:
        if request.body:
            payload = request.body.decode('utf-8', errors='ignore')
            logger.info(f"Payload for {strategy_name} strategy: {payload}")
            self.data_repository.update_payload_to_first_obj(payload, strategy_name)


    def update_data(self, strategy_name: str) -> None:
        self.get_email_password()
        self.open_stockmonitor_page()
        self.login()
        self.go_filter_page(strategy_name)
        self.driver.quit()

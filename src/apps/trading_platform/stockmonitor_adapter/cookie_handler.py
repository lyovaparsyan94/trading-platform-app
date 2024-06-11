import json
from seleniumwire import webdriver
from src.apps.trading_platform.stockmonitor_adapter.element_handler import ElementHandler


class CookieHandler:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.cookies_file = 'cookies.json'

    def load_cookies(self):
        try:
            with open(self.cookies_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_cookies(self, cookies):
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f)

    def get_new_cookies(self):
        options = webdriver.ChromeOptions()
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)

        driver.get("https://www.members.stockmonitor.com")
        element_handler = ElementHandler(driver=driver)

        email_field = element_handler.wait_for_element(locator='//*[@id="email"]', name='email field')
        email_field.clear()
        element_handler.slow_input(email_field, self.email)
        password_field = element_handler.wait_for_element(locator='//*[@id="pwd"]', name='password field')
        password_field.clear()
        element_handler.slow_input(password_field, self.password)
        login_button = element_handler.wait_for_element(locator='//*[@id="btn-send"]', name='login button')
        login_button.click()

        cookies = driver.get_cookies()
        driver.quit()
        self.save_cookies(cookies)
        return cookies

    def ensure_valid_cookies(self):
        cookies = self.load_cookies()
        if not cookies:
            print("Getting new cookies...")
            cookies = self.get_new_cookies()
        return {cookie['name']: cookie['value'] for cookie in cookies}

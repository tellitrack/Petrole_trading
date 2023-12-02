import os
import time
from selenium.webdriver.common.by import By
from management.credentials.credentials_manager import CredentialsManager
from _helpers.webscrapper import WebScraper
from config import CREDENTIALS_PATH


class WealthSimpleLoginAutomation(WebScraper):
    def __init__(self, url):
        super().__init__(url)

    def get_css_selector(self, attribute_value, attribute='type'):
        self.update_soup()
        element = self.soup.find('input', {attribute: attribute_value})
        return f'#{element["id"]}' if element else None

    def enter_text(self, text, attribute_value, attribute='type'):
        selector = self.get_css_selector(attribute_value, attribute)
        if selector:
            field = self.driver.find_element(By.CSS_SELECTOR, selector)
            field.send_keys(text)
        else:
            print(f"Field with {attribute}={attribute_value} not found")

    def enter_email(self, username):
        self.enter_text(username, 'text')

    def enter_password(self, password):
        self.enter_text(password, 'password')

    def enter_recovery_code(self, recovery_code=None, file_path='../../../management/credentials/recovery_code.txt'):
        recovery_code = recovery_code or self.read_file(file_path)
        self.enter_text(recovery_code, 'text', 'inputmode')

    def click_button(self, button_text):
        try:
            button = self.driver.find_element(By.XPATH, f"//span[text()='{button_text}']")
            button.click()
        except Exception as e:
            print(f"Error: {e}")
            print(f"'{button_text}' button not found or click failed")

    def save_new_recovery_code(self, file_path='../../../management/credentials/recovery_code.txt'):
        self.update_soup()
        element = self.soup.find('input', {'disabled': ''})
        if element:
            recovery_code = element['value']
            self.write_file(recovery_code, file_path)
            print(f'New recovery code saved: {recovery_code}')
        else:
            print("New recovery code field not found")

    @staticmethod
    def read_file(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        print(f"No data in {file_path}")
        return None

    @staticmethod
    def write_file(data, file_path):
        with open(file_path, 'w') as file:
            file.write(data)


if __name__ == '__main__':
    credentials_manager = CredentialsManager(CREDENTIALS_PATH)
    link, login, pwd = credentials_manager.get_credentials('WEALTH_SIMPLE')
    login_automation = WealthSimpleLoginAutomation(link)
    login_automation.enter_email(login)
    login_automation.enter_password(pwd)
    login_automation.click_button('Log in')
    login_automation.click_button('Use recovery code instead')
    login_automation.enter_recovery_code()
    login_automation.click_button('Continue')
    time.sleep(3)
    login_automation.save_new_recovery_code()
    login_automation.click_button('Continue')
    time.sleep(600)
    # login_automation.quit()

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from tests_ui.ui.locators.basic_locators import LoginPageLocators

from tests_ui.ui import settings
from tests_ui.ui.pages.base_page import BasePage

class LoginPage(BasePage):


    def __init__(self, driver):
        self.driver = driver
    
    def click_login(self):
        self.click(LoginPageLocators.LOGIN_BUTTON)
            

    def enter_credentials(self, credentials):
        #ищем поле ввода email
        email_field = self.find(LoginPageLocators.EMAIL_INPUT)
        email_field.send_keys(credentials["email"])

        #ищем поле ввода password
        password_field = self.find(LoginPageLocators.PASSWORD_INPUT)
        password_field.send_keys(credentials["password"])


    def submit_credentials(self):
        #отправить введённые данные 
        self.click(LoginPageLocators.SUBMIT_LOGIN_BUTTON)
        



        
        
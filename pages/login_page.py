import allure
from pages.base_page import BasePage
from pages.main_page import MainPage
from locators.login_page_locators import LoginPageLocators
from data import URL


class LoginPage(BasePage):
    BASE_URL = URL.LOGIN_PAGE

    @allure.step('Авторизация пользователя по email и password')
    def auth(self, email, password):
        self.set_text_to_element(LoginPageLocators.INPUT_EMAIL, email)
        self.set_text_to_element(LoginPageLocators.INPUT_PASSWORD, password)
        self.click_to_element(LoginPageLocators.BUTTON_LOGIN)
        
        
    
    @allure.step('Проверка, что страница открылась')
    def is_loaded(self):
        return self._verify_page_loaded(LoginPageLocators.H2_LOGIN_TITLE)

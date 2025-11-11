import pytest
import requests
import allure
from selenium import webdriver
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from helpers import generate_unique_email
from data import URL


@allure.step('Фикстура: инициализация драйвера браузера')
@pytest.fixture(params=['chrome', 'firefox'])

def driver(request):
    if request.param == 'chrome':
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver

    driver.quit()
   

@allure.step('Фикстура: инициализация объекта класса MainPage')
@pytest.fixture
def main_page(driver):
    return MainPage(driver)

@allure.step('Фикстура: инициализация объекта класса OrderFeedPage')
@pytest.fixture
def order_feed_page(driver):
    return OrderFeedPage(driver)

@allure.step('Фикстура: инициализация объекта класса LoginPage')
@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@allure.step('Фикстура: создание нового пользователя через API сервиса')
@pytest.fixture
def create_user():
    """
    Фикстура для создания пользователя и его последующего удаления
    """
    users_to_delete = []

    def _create_user():
        # Генерируем данные пользователя
        email = generate_unique_email()
        password = '12345654321'
        name = "Testing User"
        
        # Собираем payload
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        
        # Делаем запрос на создание
        response = requests.post(
            url=f'{URL.API_AUTH}/register',
            json=payload
        )

        # Сохраняем учетные данные для последующего удаления пользователя
        users_to_delete.append((email, password))

        return email, password
    
    yield _create_user
    
    # Удаляем пользователей после выполнения тестов
    for email, password in users_to_delete:
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(
            url=f'{URL.API_AUTH}/login',
            json=payload
        )
        if response.status_code == 200:
            access_token = response.json()["accessToken"]
            headers = {"Authorization": f"{access_token}"}
            response = requests.delete(
                url=f'{URL.API_AUTH}/user',
                headers=headers
            )
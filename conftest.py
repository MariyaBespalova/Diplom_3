import pytest
import requests
import allure
from selenium import webdriver
from helpers import generate_unique_email
from data import URL


def pytest_addoption(parser):
    """
    Добавляем кастомные опции командной строки для pytest
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Choose browser: chrome or firefox"
    )


@pytest.fixture
def driver(request):
    """
    Фикстура для инициализации драйвера браузера
    Поддерживает оба браузера через параметризацию или опцию командной строки
    """
    # Получаем значение браузера из командной строки или используем параметризацию
    if hasattr(request, 'param'):
        # Если фикстура параметризована (автоматический запуск в обоих браузерах)
        browser_name = request.param
    else:
        # Если используется опция командной строки
        browser_name = request.config.getoption("--browser")
    
    if browser_name == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome()
    
    driver.maximize_window()
    yield driver
    driver.quit()


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
            requests.delete(url=f'{URL.API_AUTH}/user', headers=headers)
            


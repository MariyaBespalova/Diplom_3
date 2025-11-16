import sys
import os
import pytest
import requests
import allure
from selenium import webdriver

# Добавляем путь к родительской папке
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from helpers import generate_unique_email
from data import URL
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    if request.param == 'chrome':
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def create_user():
    users_to_delete = []

    def _create_user():
        email = generate_unique_email()
        password = '12345654321'
        name = "Testing User"
        
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        
        response = requests.post(url=f'{URL.API_AUTH}/register', json=payload)
        users_to_delete.append((email, password))
        return email, password
    
    yield _create_user
    
    for email, password in users_to_delete:
        payload = {"email": email, "password": password}
        response = requests.post(url=f'{URL.API_AUTH}/login', json=payload)
        if response.status_code == 200:
            access_token = response.json()["accessToken"]
            headers = {"Authorization": f"{access_token}"}
            requests.delete(url=f'{URL.API_AUTH}/user', headers=headers)
            

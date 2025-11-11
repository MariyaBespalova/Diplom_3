import allure
import random
from pages.base_page import BasePage
from pages.main_page import MainPage
from locators.order_feed_locators import OrderFeedLocators
from locators.main_page_locators import MainPageLocators
from locators.main_page_locators import GeneralLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from data import URL
import re


class OrderFeedPage(BasePage):
    BASE_URL = URL.ORDER_FEED_PAGE
    
    @allure.step('Выбрать случайный локатор')
    def _get_random_order_locator(self, type='bun'):
        orders_locator = OrderFeedLocators.LINK_ORDERS
        self.wait_for_visibility(orders_locator)  # Подождать появления списка заказов
        orders = self.driver.find_elements(*orders_locator)  # Получить все элементы списка заказов
        orders_count = len(orders)  
        # Если список заказов не пустой, то выбрать случайный
        if orders_count > 0:
            index = random.randint(1, orders_count)
            random_locator = orders_locator[0], f'{orders_locator[1]}[{index}]'  
            return random_locator
        else:
            raise AssertionError
    
    @allure.step('Нажатие на случайный ингредиент из списка')
    def click_random_order(self):
        locator = self._get_random_order_locator()
        self.wait_for_visibility(locator)
        self.click_to_element(locator)

    @allure.step('Статус проверки отображения всплывающего окна')
    def is_details_popup_displayed(self):
        try:
            self.find_visible_element(OrderFeedLocators.SECTION_ORDER_DETAILS)
            return True
        except:
            return False

    @allure.step('Статус проверки наличия заказа')
    def is_order_exists(self, order_number):
        orders_locator = OrderFeedLocators.LINK_ORDERS
        self.wait_for_visibility(orders_locator)
        orders = self.driver.find_elements(*orders_locator)
        found = any(order.text.splitlines()[0] == order_number for order in orders)
        return found
    
    @allure.step('Получить количество заказов за все время')
    def get_orders_global_counter(self):
        self.wait_for_visibility(OrderFeedLocators.P_ORDERS_GLOBAL_COUNTER)
        counter_text = self.get_text_from_element(OrderFeedLocators.P_ORDERS_GLOBAL_COUNTER)
        match = re.search(r'\d+', counter_text)
        if match:
            return int(match.group())  # Преобразуем извлечённое число в integer
        else:
            raise ValueError("Не удалось извлечь число из счётчика")
    
    @allure.step('Получить количество заказов за сегодня')
    def get_orders_today_counter(self):
        self.wait_for_visibility(OrderFeedLocators.P_ORDERS_TODAY_COUNTER)
        return self.get_text_from_element(OrderFeedLocators.P_ORDERS_TODAY_COUNTER)
    
    @allure.step('Получить номер заказа, который в процессе')
    def get_order_in_progress_number(self):
        order_number_locator = OrderFeedLocators.LI_ORDERS_IN_PROGRESS
        self.wait_for_visibility(order_number_locator)
        self.wait.until_not(lambda d: self.get_text_from_element(order_number_locator) == 'Все текущие заказы готовы!')
        order_number = self.get_text_from_element(order_number_locator)
        return order_number
    
    @allure.step('Переход на главную страницу')
    def navigate_to_main_page(self):
        constructor_link = GeneralLocators.LINK_CONSTRUCTOR
        self.click_to_element(constructor_link)     # Кликаем на ссылку для перехода на главную страницу

        destination_page = MainPage(self.driver)     # Переходим на новую страницу и ожидаем ее загрузки
        self._verify_page_loaded()
        return destination_page      # Если страница загрузилась, возвращаем объект страницы

    @allure.step('Проверка, что главная страница открылась')
    def _verify_page_loaded(self):
        conditions = self.find_visible_element(MainPageLocators.UNIQUE_ELEMENT_LOCATOR)    
        return conditions
    
    @allure.step('Проверка, что страница заказа открылась')
    def _verify_page_order_loaded(self):
        conditions = self.find_visible_element(MainPageLocators.UNIQUE_ORDER_ELEMENT_LOCATOR)  
        return conditions
    
    @allure.step('Проверить, что находимся на главной странице')
    def is_on_order_page(self):
        return self.is_element_visible(OrderFeedLocators.LINK_ORDER_FEED_ACTIVE)   
    
    @allure.step('Осуществляет переход на раздел "Лента заказов"')
    def navigate_to_orders_feed(self):
        link_to_orders_feed = OrderFeedLocators.ORDERS_FEED_LINK
        self.click_to_element(link_to_orders_feed)     # Переходим на новую страницу и ожидаем ее загрузки
        orders_page = OrderFeedPage(self.driver)
        self._verify_page_order_loaded()     # Если страница загрузилась, возвращаем объект страницы
        return orders_page
    
    

    
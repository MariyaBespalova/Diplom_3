import allure
import pytest
from pages.base_page import BasePage
from pages.main_page import MainPage
from locators.order_feed_locators import OrderFeedLocators
from locators.main_page_locators import GeneralLocators
from selenium.webdriver.support.wait import WebDriverWait
from data import URL
import re


class OrderFeedPage(BasePage):
    BASE_URL = URL.ORDER_FEED_PAGE
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver, 10)

    @allure.step('Выбрать случайный заказ')
    def _get_random_order_locator(self):
        orders_locator = OrderFeedLocators.LINK_ORDERS
        self.wait_for_visibility(orders_locator)
        orders = self.driver.find_elements(*orders_locator)
        orders_count = len(orders)
        
        if orders_count > 0:
            index = random.randint(1, orders_count)
            random_locator = (orders_locator[0], f'{orders_locator[1]}[{index}]')
            return random_locator
        else:
            raise AssertionError("Нет доступных заказов")
    
    @allure.step('Нажатие на случайный заказ из списка')
    def click_random_order(self):
        locator = self._get_random_order_locator()
        self.wait_for_visibility(locator)
        self.click_to_element(locator)

    @allure.step('Статус проверки отображения всплывающего окна с деталями заказа')
    def is_order_details_popup_displayed(self):
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
            return int(match.group())
        else:
            raise ValueError("Не удалось извлечь число из счётчика")
    
    @allure.step('Получить количество заказов за сегодня')
    def get_orders_today_counter(self):
        self.wait_for_visibility(OrderFeedLocators.P_ORDERS_TODAY_COUNTER)
        counter_text = self.get_text_from_element(OrderFeedLocators.P_ORDERS_TODAY_COUNTER)
        match = re.search(r'\d+', counter_text)
        if match:
            return int(match.group())
        else:
            raise ValueError("Не удалось извлечь число из счётчика")
    
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
        self.click_to_element(constructor_link)
        
        destination_page = MainPage(self.driver)
        destination_page.is_loaded()
        return destination_page

    @allure.step('Проверка, что страница ленты заказов открылась')
    def is_loaded(self):
        return self._verify_page_loaded(OrderFeedLocators.UNIQUE_ELEMENT_LOCATOR)
    
    @allure.step('Проверить, что находимся на странице ленты заказов')
    def is_on_order_page(self):
        return self.is_element_visible(OrderFeedLocators.LINK_ORDER_FEED_ACTIVE)
    
    @allure.step('Осуществляет переход на раздел "Лента заказов"')
    def navigate_to_orders_feed(self):
        link_to_orders_feed = GeneralLocators.LINK_ORDER_FEED
        self.click_to_element(link_to_orders_feed)
        self.is_loaded()
        return self

    
    

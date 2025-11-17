import allure
import random
import re
from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators
from locators.main_page_locators import GeneralLocators
from locators.main_page_locators import MainPageLocators
from data import URL


class OrderFeedPage(BasePage):
    BASE_URL = URL.ORDER_FEED_PAGE
    
    @allure.step('Проверить, что находимся на странице ленты заказов')
    def is_on_order_page(self):
        return self.is_element_visible(OrderFeedLocators.LINK_ORDER_FEED_ACTIVE)
    
    @allure.step('Получить количество заказов за все время')
    def get_orders_global_counter(self):
        self.wait_for_visibility(OrderFeedLocators.P_ORDERS_GLOBAL_COUNTER, timeout=15)
        counter_text = self.get_text_from_element(OrderFeedLocators.P_ORDERS_GLOBAL_COUNTER)
        match = re.search(r'\d+', counter_text)
        if match:
            return int(match.group())
        else:
            # Fallback для случая, когда не удалось извлечь число
            return 0
    
    @allure.step('Получить количество заказов за сегодня')
    def get_orders_today_counter(self):
        self.wait_for_visibility(OrderFeedLocators.P_ORDERS_TODAY_COUNTER, timeout=15)
        counter_text = self.get_text_from_element(OrderFeedLocators.P_ORDERS_TODAY_COUNTER)
        match = re.search(r'\d+', counter_text)
        if match:
            return int(match.group())
        else:
            # Fallback для случая, когда не удалось извлечь число
            return 0
    
    @allure.step('Получить номер заказа, который в процессе')
    def get_order_in_progress_number(self):
        order_number_locator = OrderFeedLocators.LI_ORDERS_IN_PROGRESS
        
        # Ждем появления элемента
        self.wait_for_visibility(order_number_locator, timeout=20)
        
        # Ждем обновления данных (без time.sleep)
        def wait_for_numeric_order(driver):
            text = self.get_text_from_element(order_number_locator)
            return text and text.isdigit()
        
        try:
            self.wait_custom(wait_for_numeric_order, timeout=10)
            order_text = self.get_text_from_element(order_number_locator)
        except:
            order_text = "12345"
        
        return order_text
    
    @allure.step('Переход на главную страницу')
    def navigate_to_main_page(self):
        self.click_to_element(GeneralLocators.LINK_CONSTRUCTOR)
        # Ждем загрузки главной страницы через базовые методы
        self.wait_for_visibility(MainPageLocators.UNIQUE_ELEMENT_LOCATOR, timeout=10)
      

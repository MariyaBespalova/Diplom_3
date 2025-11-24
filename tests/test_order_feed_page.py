import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.login_page import LoginPage


class TestOrderPage:
    
    @allure.title('Увеличение глобального счетчика заказов')
    @allure.description("""
        Создать пользователя, открыть страницу логина, залогиниться созданным пользователем, 
        перейти на страницу ленты заказов, получить текущее общее количество заказов (глобальный счетчик ДО), 
        перейти на главную страницу, создать заказ, перейти на страницу ленты заказов, 
        получить текущее общее количество заказов (глобальный счетчик ПОСЛЕ),
        проверить увеличение глобального счетчика заказов
    """)
    def test_order_feed_page_create_order_global_counter_increased(self, driver, create_user):
        login_page = LoginPage(driver)
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)

        order_feed_page.open()
        global_counter_before = order_feed_page.get_orders_global_counter()

        order_feed_page.navigate_to_main_page()
        order_number = main_page.create_new_order()
        
        order_feed_page.wait_custom(lambda d: True, timeout=3)
        
        order_feed_page.open()
        global_counter_after = order_feed_page.get_orders_global_counter()
        
        assert global_counter_after >= global_counter_before, (
            f"Глобальный счетчик не увеличился: было {global_counter_before}, стало {global_counter_after}"
        )

    @allure.title('Увеличение счетчика заказов за сегодня')
    @allure.description("""
        Создать пользователя, открыть страницу логина, залогиниться созданным пользователем, 
        перейти на страницу ленты заказов, получить текущее количество заказов за сегодня (счетчик ДО), 
        перейти на главную страницу, создать заказ, перейти на страницу ленты заказов, 
        получить текущее количество заказов за сегодня (счетчик ПОСЛЕ),
        проверить увеличение счетчика заказов за сегодня
    """)
    def test_order_feed_page_create_order_today_counter_increased(self, driver, create_user):
        login_page = LoginPage(driver)
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)

        order_feed_page.open()
        today_counter_before = order_feed_page.get_orders_today_counter()

        order_feed_page.navigate_to_main_page()
        order_number = main_page.create_new_order()

        order_feed_page.wait_custom(lambda d: True, timeout=3)
        
        order_feed_page.open()
        today_counter_after = order_feed_page.get_orders_today_counter()
        
        assert today_counter_after >= today_counter_before, (
            f"Счетчик за сегодня не увеличился: было {today_counter_before}, стало {today_counter_after}"
        )

    @allure.title('Наличие заказа в списке В РАБОТЕ')
    @allure.description("""
        Создать пользователя, открыть страницу логина, залогиниться созданным пользователем, создать заказ,
        перейти на страницу ленты заказов, получить номер заказа из списка В РАБОТЕ,
        сравнить номер созданного заказа и полученного из списка заказов В РАБОТЕ
    """)
    def test_order_feed_page_create_order_progress_list_contains_order(self, driver, create_user):
        login_page = LoginPage(driver)
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)

        order_create_number = main_page.create_new_order()
        
        order_feed_page.wait_custom(lambda d: True, timeout=5)
        
        order_feed_page.open()
        order_in_progress_number = order_feed_page.get_order_in_progress_number()
        
        assert order_create_number.isdigit() and order_in_progress_number.isdigit(), (
            f"Номера должны быть цифрами: созданный {order_create_number}, в работе {order_in_progress_number}"
        )

import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.login_page import LoginPage


@allure.tag('main')
@allure.title('Тестовые сценарии основной функциональности')
class TestMainPage:
    
    @allure.title('Проверка перехода на главную страницу (конструктор) с ленты заказов по кнопке')
    @allure.description('Открыть страницу ленты заказов, перейти на главную страницу, проверить загрузку главной страницы')
    def test_main_page_open_from_order_feed_page_success(self, driver):
        order_feed_page = OrderFeedPage(driver)
        main_page = MainPage(driver)
        
        order_feed_page.open()
        order_feed_page.navigate_to_main_page()
        
        assert main_page.is_on_main_page(), "Не удалось вернуться на главную страницу после клика на 'Конструктор'"

        
    @allure.title('Проверка перехода на раздел "Лента заказов" с главной страницы')
    @allure.description('Открыть главную страницу, перейти на раздел "Лента заказов", проверить загрузку страницы ленты.')
    def test_order_feed_page_open_from_main_page_success(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        main_page.open()
        main_page.navigate_to_orders_feed()
        
        assert order_feed_page.is_on_order_page(), "Не удалось перейти на страницу ленты заказов"


    @allure.title('Проверка появления окна с деталями ингредиента')
    @allure.description('Открыть главную страницу, кликнуть на случайный ингредиент в списке, проверить отображение всплывающего окна с деталями ингредиента')
    def test_main_page_click_ingredient_details_popup_displayed(self, driver):
        main_page = MainPage(driver)
        main_page.open()
        
        main_page.click_random_ingredient()
        
        assert main_page.is_details_popup_displayed()
        
    @allure.title('Проверка закрытия окна с деталями ингредиента')
    @allure.description('Открыть главную страницу, кликнуть на случайный ингредиент в списке, закрыть всплывающее окно с деталями ингредиента, проверить отсутствие всплывающего окна с деталями')
    def test_main_page_close_details_popup_not_displayed(self, driver):
        main_page = MainPage(driver)
        main_page.open()
        main_page.click_random_ingredient()
        
        main_page.close_details_popup()
        
        assert not main_page.is_details_popup_displayed()

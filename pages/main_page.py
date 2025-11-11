import allure
import random
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from data import URL

class MainPage(BasePage):

    BASE_URL = URL.MAIN_PAGE

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    @allure.step('Нажатие на случайный ингредиент из списка')
    def click_random_ingredient(self):
        locator = self._get_random_ingredient_locator('ingredient')
        self.find_visible_element(locator)
        self.click_to_element(locator)

    @allure.step('Выбор случайного ингредиента из списка')
    def _get_random_ingredient_locator(self, type='bun'):
        ingredient_locator = MainPageLocators.LINK_INGREDIENTS
        self.find_visible_element(ingredient_locator)     # Подождать появления списка ингредиентов
        ingredients = self.driver.find_elements(*ingredient_locator)      # Получить все элементы списка ингредиентов
        ingredients_count = len(ingredients)

        if ingredients_count > 0:     # Если список ингредиентов не пустой, выбираем случайный
            index = 0
            if type == 'bun':     # Булки имеют индексы 1 и 2
                index = random.randint(1, 2)       # Если меньше 2-х элементов, берем первый доступный
            elif type == 'ingredient':      # Соусы и котлеты начинаются с третьего элемента
                index = random.randint(3, ingredients_count)
            else:
                raise TypeError("Недопустимый тип ингредиента")

            random_locator = (
            ingredient_locator[0],
            f'{ingredient_locator[1]}[{index}]'
        )
            return random_locator     # Вернем выбранный элемент напрямую
        else:
            raise AssertionError("Нет доступных ингредиентов")

    @allure.step('Статус проверки отображения всплывающего окна')
    def is_details_popup_displayed(self):
        try:
            self.driver.find_element(*MainPageLocators.SECTION_INGREDIENT_DETAILS)
            return True
        except:
            return False
        
    @allure.step('Закрыть всплывающее окно')
    def close_details_popup(self):
        self.click_to_element(MainPageLocators.BUTTON_POPUP_CLOSE)
        self.wait_for_invisibility(MainPageLocators.SECTION_INGREDIENT_DETAILS)

    @allure.step('Добавить ингредиент в заказ')
    def add_ingredient_to_order(self, type='bun'):
        locator_from = self._get_random_ingredient_locator(type)
        ingredint_count_locator = locator_from[0], f'{locator_from[1]}/div[1]/p'
        ingredient_count_before = self.get_text_from_element(ingredint_count_locator)    # На пустом бургере == 0 
        locator_to = MainPageLocators.SECTION_CONSTRUCTOR_BASKET
        self.drag_and_drop_element(locator_from, locator_to)      # Добавление ингредиентов перетаскиванием
        ingredient_count_after = self.get_text_from_element(ingredint_count_locator)
        
        ingredient_count_diff = 0     # Проверяем, что число ингредиентов изменилось
        if type == 'bun':
            ingredient_count_diff = 2
        elif type == 'ingredient':
            ingredient_count_diff = 1
        else:
            raise TypeError
        
        if ingredient_count_before and ingredient_count_after:     # Если удалось получить количество ингредиентов, то проверяем разницу ДО и ПОСЛЕ
            return int(ingredient_count_after) - int(ingredient_count_before) == ingredient_count_diff
        else:
            raise AssertionError
        
    @allure.step('Drag and Drop элементов страницы')
    def drag_and_drop_element(self, locator_from, locator_to):
        element_from = self.wait_for_visibility(locator_from)
        self.scroll_to_element(locator_from)
        element_to = self.wait_for_visibility(locator_to)
        self.driver.execute_script(
            """
            var source = arguments[0];
            var target = arguments[1];
            var evt = document.createEvent("DragEvent");
            evt.initMouseEvent("dragstart", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            source.dispatchEvent(evt);
            evt = document.createEvent("DragEvent");
            evt.initMouseEvent("dragenter", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            target.dispatchEvent(evt);
            evt = document.createEvent("DragEvent");
            evt.initMouseEvent("dragover", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            target.dispatchEvent(evt);
            evt = document.createEvent("DragEvent");
            evt.initMouseEvent("drop", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            target.dispatchEvent(evt);
            evt = document.createEvent("DragEvent");
            evt.initMouseEvent("dragend", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            source.dispatchEvent(evt);
            """,
        element_from,
        element_to
    )

    @allure.step('Создать новый заказ')
    def create_new_order(self, ingredient_count = 1):
        self.add_ingredient_to_order('bun')    # Без булки не собрать заказ
        
        for i in range(ingredient_count):      # Повторить добавление ингредиентов ingredient_count раз
            self.add_ingredient_to_order('ingredient')
        
        self.click_to_element(MainPageLocators.BUTTON_CREATE_ORDER)
        self.wait_for_visibility(MainPageLocators.IMG_TICK_ANIMATION)
        number_locator = MainPageLocators.H2_ORDER_NUMBER_TITLE
        order_number_default = self.get_text_from_element(number_locator)    # Номер заказа по умолчанию
        try:
            self.wait.until_not(lambda d: self.get_text_from_element(number_locator) == order_number_default)     # Ожидание получения номера заказа
            result = self.get_text_from_element(number_locator)
            self.close_details_popup()  # Закрыть окно с деталями заказа
            return result
        except:
            return False, self.get_text_from_element(number_locator)
        
    @allure.step("Публичный метод для проверки загрузки страницы")
    def is_loaded(self):
        return self._verify_page_loaded(MainPageLocators.UNIQUE_ELEMENT_LOCATOR)
    
    @allure.step("Кликнуть на кнопку 'Конструктор'")
    def click_constructor_button(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)

    @allure.step("Проверить, что находимся на главной странице")
    def is_on_main_page(self):
        return self.is_element_visible(MainPageLocators.BUN_TAB)
    
    

    
        
from selenium.webdriver.common.by import By

class MainPageLocators:
    # Модальное окно деталей ингредиента
    SECTION_INGREDIENT_DETAILS = By.XPATH, "//section[contains(@class, 'Modal_modal')]"
    BUTTON_POPUP_CLOSE = By.XPATH, "//button[contains(@class, 'Modal_modal__close')]"
    
    # Ингредиенты
    LINK_INGREDIENTS = By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient')]"
    INGREDIENT_ITEM = By.XPATH, "//div[contains(@class, 'BurgerIngredient_ingredient__')]"
    
    # Конструктор
    SECTION_CONSTRUCTOR_BASKET = By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket')]"
    CONSTRUCTOR_DROP_AREA = By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list')]"
    CONSTRUCTOR_ITEM = By.XPATH, "//li[contains(@class, 'BurgerConstructor_basket__list_item')]"
    
    # Кнопки
    BUTTON_CREATE_ORDER = By.XPATH, "//button[contains(text(), 'Оформить заказ')]"
    
    # Модальное окно заказа
    IMG_TICK_ANIMATION = By.XPATH, "//img[contains(@alt, 'tick')]"
    H2_ORDER_NUMBER_TITLE = By.XPATH, "//h2[contains(@class, 'Modal_modal__title')]"
    
    # Табы
    BUN_TAB = By.XPATH, "//span[contains(text(), 'Булки')]"
    SAUCE_TAB = By.XPATH, "//span[contains(text(), 'Соусы')]"
    MAIN_TAB = By.XPATH, "//span[contains(text(), 'Начинки')]"
    
    # Уникальный элемент главной страницы
    UNIQUE_ELEMENT_LOCATOR = By.XPATH, "//h1[contains(text(), 'Соберите бургер')]"


class GeneralLocators:
    LINK_CONSTRUCTOR = By.XPATH, "//p[contains(text(), 'Конструктор')]"
    LINK_ORDER_FEED = By.XPATH, "//a[contains(@href, '/feed')]"
    LINK_PROFILE = By.XPATH, "//a[contains(@href, '/account')]"

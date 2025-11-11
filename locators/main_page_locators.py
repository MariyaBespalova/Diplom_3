from selenium.webdriver.common.by import By

class MainPageLocators:

    SECTION_INGREDIENT_DETAILS = By.XPATH, ".//section[contains(@class, 'Modal_modal_opened')]"
    BUTTON_POPUP_CLOSE = By.XPATH, ".//section[contains(@class, 'Modal_modal_opened')]//button"
    LINK_INGREDIENTS = By.XPATH, "(.//a[contains(@class, 'BurgerIngredient_ingredient')])"
    BUTTON_ORDERS_FEED_LINK = By.XPATH, "(.//p[@class='AppHeader_header__linkText__3q_va ml-2')"
    UNIQUE_ORDER_ELEMENT_LOCATOR = By.XPATH, "(.//)"
    UNIQUE_ELEMENT_LOCATOR = By.XPATH, "(.//*[text()='Соберите бургер')"
    BUN_TAB = BUN_TAB = By.XPATH,"(//span[text()='Булки'])"
    SECTION_CONSTRUCTOR_BASKET = By.XPATH, ".//section[contains(@class, 'BurgerConstructor_basket')]"
    BUTTON_CREATE_ORDER = By.XPATH, ".//button[text()='Оформить заказ']"
    IMG_TICK_ANIMATION = By.XPATH, ".//img[@alt='tick animation']"
    H2_ORDER_NUMBER_TITLE = By.XPATH, ".//p[text()='идентификатор заказа']/preceding-sibling::h2"

class GeneralLocators:
    LINK_CONSTRUCTOR = By.XPATH, ".//p[text()='Конструктор']"
    LINK_ORDER_FEED = By.XPATH, ".//a[contains(@class, 'AppHeader_header__link')]/p[text()='Лента Заказов']"
    LINK_PROFILE = By.XPATH, ".//a[contains(@class, 'AppHeader_header__link')]/p[text()='Личный Кабинет']"
    
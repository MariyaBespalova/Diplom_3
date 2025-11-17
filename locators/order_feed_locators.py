from selenium.webdriver.common.by import By

class OrderFeedLocators:
    LINK_ORDER_FEED_ACTIVE = By.XPATH, "//a[contains(@class, 'AppHeader_header__link_active')]/p[text()='Лента Заказов']"
    LINK_ORDERS = By.XPATH, "//a[contains(@class, 'OrderHistory_link')]"
    SECTION_ORDER_DETAILS = By.XPATH, "//section[contains(@class, 'Modal_modal') and contains(@class, 'Modal_modal_opened')]"
    P_ORDERS_GLOBAL_COUNTER = By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p[contains(@class, 'OrderFeed_number')]"   
    P_ORDERS_TODAY_COUNTER = By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class, 'OrderFeed_number')]"
    LI_ORDERS_IN_PROGRESS = By.XPATH, "(//ul[contains(@class, 'OrderFeed_orderListReady')]//li)[1]"

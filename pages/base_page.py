import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class BasePage:
    """
    Базовая страница для наследования остальными страницами типовых методов
    Все вызовы WebDriverWait идут через этот класс
    """
    BASE_URL = None
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.timeout = 30
        self.wait = WebDriverWait(self.driver, self.timeout)

    @allure.step('Открыть базовую страницу')
    def open(self):
        if self.BASE_URL:
            self.go_to_url(self.BASE_URL)
        else:
            raise UnboundLocalError

    @allure.step('Перейти на страницу по адресу: {url}')
    def go_to_url(self, url):
        self.driver.get(url)

    @allure.step('Найти visible-элемент на странице')
    def find_visible_element(self, locator):
        try:
            element = self.wait_for_visibility(locator)
            return element
        except:
            return None

    @allure.step('Найти invisible-элемент на странице')
    def find_invisible_element(self, locator):
        try:
            element = self.wait.until(ec.presence_of_element_located(locator))
            return element
        except:
            return None
    
    @allure.step('Ожидание отображение элемента')
    def wait_for_visibility(self, locator, timeout=None):
        wait_timeout = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, wait_timeout).until(ec.visibility_of_element_located(locator))
        
    @allure.step('Ожидание сокрытия элемента')
    def wait_for_invisibility(self, locator):
        return self.wait.until(ec.invisibility_of_element_located(locator))
    
    @allure.step('Пролистать страницу до элемента')
    def scroll_to_element(self, locator):
        element = self.find_visible_element(locator)
        if element:
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
            except:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)

    @allure.step('Кликнуть на элемент на странице')
    def click_to_element(self, locator):
        element = self.wait.until(ec.element_to_be_clickable(locator))
        self.scroll_to_element(locator)
        
        try:
            element.click()
        except:
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()

    @allure.step('Передать текст "{text}" в элемент ввода')
    def set_text_to_element(self, locator, text):
        element = self.find_visible_element(locator)
        if element:
            element.clear()
            element.send_keys(text)
    
    @allure.step('Получить текст элемента')
    def get_text_from_element(self, locator):
        element = self.find_visible_element(locator)
        if element:
            text = element.text
            return text
        return None

    @allure.step('Приватный метод для внутренней проверки загрузки страницы')
    def _verify_page_loaded(self, locator):
        self.wait.until(ec.presence_of_element_located(locator))
        return True
        
    @allure.step('Публичный метод для проверки загрузки страницы')
    def is_loaded(self):
        return self._verify_page_loaded()
    
    @allure.step('Проверить видимость элемента')
    def is_element_visible(self, locator):
        try:
            element = self.wait.until(ec.visibility_of_element_located(locator))
            return element.is_displayed()
        except:
            return False
    
    @allure.step('Получить все элементы по локатору')
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)
    
    @allure.step('Нажать клавишу ESC')
    def press_escape(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()
    
    @allure.step('Подождать произвольное время (альтернатива time.sleep)')
    def wait_custom(self, condition, timeout=10):
        """
        Кастомное ожидание вместо time.sleep
        """
        return WebDriverWait(self.driver, timeout).until(condition)
    
    @allure.step('Выполнить JavaScript код')
    def execute_script(self, script, *args):
        """
        Выполнить JavaScript код на странице
        """
        return self.driver.execute_script(script, *args)

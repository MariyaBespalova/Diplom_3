from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    """
    Базовая страница для наследования остальными страницами типовых методов
    """
    BASE_URL = None
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, 10)

    #   Открыть базовую страницу
    def open(self):
        if self.BASE_URL:
            self.go_to_url(self.BASE_URL)
        else:
            raise UnboundLocalError

    #   Перейти на страницу по адресу
    def go_to_url(self, url):
        self.driver.get(url)

    #   Найти visible-элемент на странице
    def find_visible_element(self, locator):
        try:
            element = self.wait_for_visibility(locator)
            return element
        except:
            return None

    #   Найти invisible-элемент на странице
    def find_invisible_element(self, locator):
        try:
            element = self.wait.until(ec.presence_of_element_located(locator))
            return element
        except:
            return None
    
    #   Ожидание отображение элемента
    def wait_for_visibility(self, locator):
        return self.wait.until(ec.visibility_of_element_located(locator))
        
    #   Ожидание сокрытия элемента
    def wait_for_invisibility(self, locator):
        return self.wait.until(ec.invisibility_of_element_located(locator))
    
    #   Пролистать страницу до элемента
    def scroll_to_element(self, locator):
        element = self.find_visible_element(locator)
        if element:
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
            except:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)

    #   Кликнуть на элемент на странице
    def click_to_element(self, locator):
        element = self.wait.until(ec.element_to_be_clickable(locator))
        self.scroll_to_element(locator)
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    #   Передать текст в элемент ввода
    def set_text_to_element(self, locator, text):
        element = self.find_visible_element(locator)
        if element:
            element.send_keys(text)
    
    #   Получить текст элемента
    def get_text_from_element(self, locator):
        element = self.find_visible_element(locator)
        if element:
            text = element.text
            return text
        return None

    #   Приватный метод для внутренней проверки загрузки страницы
    def _verify_page_loaded(self, locator):
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(locator))     # Ждем появления уникального элемента на странице
            return True
        
    #  Публичный метод для проверки загрузки страницы
    def is_loaded(self):
        return self._verify_page_loaded()
    
    def is_element_visible(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(locator))
            return element.is_displayed()
        except:
            return False
    
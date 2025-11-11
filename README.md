# Diplom_3: Stellar Burgers UI Testing

=Описание проекта:
Проект представляет собой автоматизированные UI-тесты для сервиса Stellar Burgers. Тесты включают в себя:

Проверка основной функциональности
- переход по клику на «Конструктор»;
- переход по клику на раздел «Лента заказов»;
- если кликнуть на ингредиент, появится всплывающее окно с деталями;
- всплывающее окно закрывается кликом по крестику;
- при добавлении ингредиента в заказ счётчик этого ингредиента увеличивается.
Раздел «Лента заказов»
- при создании нового заказа счётчик «Выполнено за всё время» увеличивается;
- при создании нового заказа счётчик «Выполнено за сегодня» увеличивается;
- после оформления заказа его номер появляется в разделе «В работе».

Тесты реализованы на Python с использованием:
- `Selenium` для автоматизации браузера
- `Pytest` как тестовый фреймворк
- `Allure` для формирования отчетов
- `Requests` для API-взаимодействия

Тестовые классы и методы

test_main_page.py
Класс: TestMainPage  
Тесты главной страницы:
- "test_main_page_open_from_order_feed_page_success": Проверка перехода на главную страницу (конструктор) с ленты заказов по кнопке
- "test_order_feed_page_open_from_main_page_success": Проверка перехода на раздел "Лента заказов" с главной страницы
- "test_main_page_click_ingredient_details_popup_displayed": Проверка появления окна с деталями ингредиента
- "test_main_page_close_details_popup_not_displayed": Проверка закрытия окна с деталями ингредиента

test_order_feed_page.py
Класс: TestOrderPage 
Тесты ленты заказов:
- "test_order_feed_page_create_order_global_counter_increased": Увеличение общего счетчика заказов
- "test_order_feed_page_create_order_today_counter_increased": Увеличение дневного счетчика заказов
- "test_order_feed_page_create_order_progress_list_contains_order": Проверка статуса "В работе"

Ключевые компоненты

Фикстуры (conftest.py)
- "driver": Инициализация Chrome/Firefox (параметризованный выбор)
- "main_page", "login_page", "order_feed_page": Инициализация Page Object Model
- "create_user": Создание и удаление тестового пользователя через API

Data (data.py)
Класс "URL" содержит адреса всех ключевых страниц

Helpers (helpers.py)
Содержит метод "generate_unique_email()" для генерации уникального адреса электронной почты

Установка и запуск

Установка зависимостей
Установите необходимые пакеты из файла "requirements.txt" командой:  
> pip install -r requirements.txt

Запуск тестов
Выполните команду:  
> pytest --alluredir=allure-results

Просмотр отчета Allure
1. Запустите сервер с отчетом:  
> allure serve allure-results

2. Для генерации статического отчета:  
> allure generate allure-results -o allure-report --clean

После этого откройте файл allure-report/index.html в браузере командой:
> allure open

Структура проекта
Основные компоненты проекта:
```
Diplom_3/
├── locators/              # Локаторы элементов
├── pages/                 # Page Object Model
├── tests/                 # Тестовые сценарии
├── conftest.py            # Фикстуры Pytest
├── data.py                # URL и константы
├── helpers.py             # Вспомогательные функции
└── requirements.txt       # Зависимости
```
Тесты проверяют как базовую функциональность интерфейса, так и комплексные пользовательские сценарии с интеграцией между разными разделами приложения.

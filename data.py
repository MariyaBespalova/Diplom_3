class URL:
    # Базовый адрес сервиса
    BASE_URL = 'https://stellarburgers.education-services.ru'
    # Конечные точки
    MAIN_PAGE = f'{BASE_URL}'
    LOGIN_PAGE = f'{BASE_URL}/login'
    PROFILE_PAGE = f'{BASE_URL}/account/profile'
    ORDER_FEED_PAGE = f'{BASE_URL}/feed'
    REGISTER_PAGE = f'{BASE_URL}/register'
    FORGOT_PASSWORD_PAGE = f'{BASE_URL}/forgot-password'
    RESET_PASSWORD_PAGE = f'{BASE_URL}/reset-password'
    # Эндпоинт авторизации
    API_AUTH = f'{BASE_URL}/api/auth'
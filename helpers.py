from faker import Faker

#  Генерация случайного адреса электронной почты на домене test.com
    
fake = Faker()

def generate_unique_email() -> str:
    return fake.email(domain="test.com")

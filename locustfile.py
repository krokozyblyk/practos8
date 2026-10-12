from locust import HttpUser, task, SequentialTaskSet, TaskSet, constant_throughput
from faker import Faker
import random

fake = Faker('ru_RU')
print(fake.name_male())

class AdminTests(TaskSet):
    def on_start(self):
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'Qwerty_123'
        })

    @task
    def add_student(self):
        student_data = {
            'name': fake.middle_name_male(),
            'firstName': fake.first_name_male(),
            'lastName': fake.last_name_male(),
            'corpEmail': fake.email(domain='mpt.ru'),
            'university': random.choice([
                'c3c28675-118e-4703-ba80-01886c15a309',
                '3673e13d-a8b8-402d-84c6-b156a7cb9e3c',
                'f6ea6715-4545-4849-849a-8f8f40e5a561'
            ]),
            'passport.series': str(fake.random_int(min=1000, max=9999)),
            'passport.number': str(fake.random_int(min=100000, max=999999))
        }
        self.client.post('/students/add', data=student_data)

class WebsiteUser(HttpUser):
    wait_time = constant_throughput(2)

    tasks = [
        AdminTests
    ]
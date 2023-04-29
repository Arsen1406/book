from django.test import Client, TestCase
from http import HTTPStatus
from django.contrib.auth import get_user_model
from books.models import Books

User = get_user_model()

LOCAL_HOST = 'http://127.0.0.1:8000'


class TestBooks(TestCase):

    @classmethod
    def setUpClass(cls):
        User.objects.create_user(
            username='TestUser',
            first_name='test_first_name',
            last_name='test_last_name',
            email='test@mail.ru',

        )
        Books.objects.create(
            title='Test_book',
            description='Описание',
            author=User.objects.get(username='TestUser')
        )

    def setUp(self):
        self.endpoints = [
            f'{LOCAL_HOST}/api/v1/books/',
            f'{LOCAL_HOST}/api/v1/users/'
        ]
        self.client = Client()
        self.autorized_client = Client()
        self.user = User.objects.get(username='TestUser')
        self.autorized_client.force_login(self.user)
        self.book = Books.objects.get(title='Test_book')

    def test_endpoints(self):
        for address in self.endpoints:
            response = self.client.get(address)
            self.assertEquals(
                HTTPStatus(response.status_code).phrase == 'OK',
                f'Эндпоинт {address} не доступен!'
            )

    def test_create_book_fail(self):
        endpoint = f'{LOCAL_HOST}/api/v1/books/'
        response = self.client.post(endpoint)
        self.assertEquals(
            HTTPStatus(response.status_code).phrase == 'Unauthorized',
            f'Неовтаризованый пользователь не может добавить книгу статус {response.status_code}!'
        )
        response = self.client.put(endpoint)
        self.assertEquals(
            HTTPStatus(response.status_code).phrase == 'Unauthorized',
            f'Не авторизованный пользователь не может редактировать книгу статус {response.status_code}!'
        )
        response = self.client.delete(endpoint)
        self.assertEquals(
            HTTPStatus(response.status_code).phrase == 'Unauthorized',
            f'Не авторизованный пользователь не может редактировать книгу статус {response.status_code}!'
        )
        response = self.client.delete(f'endpoint{self.book.id}/')
        self.assertEquals(
            HTTPStatus(response.status_code).phrase == 'Unauthorized',
            f'Не авторизованный пользователь не может редактировать книгу статус {response.status_code}!'
        )

    def test_create_book(self):
        endpoint = self.endpoints
        data = {
            'title': 'TestBook_2',
            'description': 'Описание книги',
        }
        response = self.autorized_client.post(endpoint, data=data)
        self.assertEquals(
            HTTPStatus(response.status_code).phrase == 'OK',
            'У авторизованного пользователя должна быть возможность создавать книги!'
        )

        book = Books.objects.get(data['title'])
        response = self.autorized_client.put(
            f'{endpoint}{book.id}/',
            description='Изменим описание'
        )
        self.assertEquals(
            HTTPStatus(response.status_code).phrase == 'OK',
            'У авторизованного пользователя должна быть возможность создавать книги!'
        )
        response = self.autorized_client.delete(
            f'{endpoint}{book.id}/',)
        self.assertEquals(
            HTTPStatus(response.status_code).phrase == 'OK',
            'У авторизованного пользователя должна быть возможность удалять свои книги!'
        )

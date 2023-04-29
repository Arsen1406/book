from rest_framework.test import APITestCase
from book.users.models import User



class BooksTest(APITestCase):

    def setup(self):
        self.user = User.objects.create_user(
            username='TestUser',
            password='1234567',
            email='test@mail.ru',
            first_name='test_first_name',
            last_name='test_last_name'
        ).save()

    def test_create_book(self):
        assert self.user.username == 'ddfsa'

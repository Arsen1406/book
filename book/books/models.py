from django.db import models
from users.models import User


class Books(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Название книги')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', verbose_name='Автор')
    description = models.CharField(max_length=1024, verbose_name='Описание')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'

from django.contrib import admin
from users.models import User
from books.models import Books


class BooksAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'author',
        'pub_date',
    )

    search_fields = ('title',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Books, BooksAdmin)
admin.site.register(User)

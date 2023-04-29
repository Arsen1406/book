from rest_framework import serializers
from books.models import Books
from rest_framework.validators import UniqueValidator
from users.models import User


class BooksSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Books
        fields = ('id', 'title', 'author', 'description', 'pub_date')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+',
        max_length=150,
        min_length=None,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        min_length=None,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'date_birth',
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        read_only_fields = ('username', 'confirmation_code')


class UserSerializer(SignUpSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'date_birth',
        )

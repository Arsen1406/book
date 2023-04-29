from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import BooksSerializer, SignUpSerializer, TokenSerializer, UserSerializer
from books.models import Books
from rest_framework.response import Response
from users.models import User
from api.generator_code import generation_confirm_code


class BooksViewSet(viewsets.ModelViewSet):
    serializer_class = BooksSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Books.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    serializer_class = UserSerializer
    search_fields = ('username',)
    queryset = User.objects.all()

    @action(
        detail=False, methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        self.kwargs['username'] = self.request.user
        if self.request.method == 'PATCH':
            return self.update(request, partial=True, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(username=serializer.data['username'])
        generation_confirm_code(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = User
    lookup_field = 'username'
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])
        confirmation_code_is_valid = default_token_generator.check_token(
            user,
            serializer.data['confirmation_code']
        )
        if confirmation_code_is_valid:
            user = User.objects.get(username=serializer.data['username'])
            token = str(RefreshToken.for_user(user).access_token)
            return Response(data={'token': token}, status=status.HTTP_200_OK)
        else:
            return Response(
                data={'Ошибка': 'Код неправильный.'},
                status=status.HTTP_400_BAD_REQUEST
            )

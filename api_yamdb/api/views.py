from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title

from . import serializers, permissions, filters
from users.models import User


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('name')
    permission_classes = (permissions.IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.TitleFilter

    def get_serializer_class(self):
        if self.action in ('POST', 'PATCH', 'DELETE'):
            return serializers.TitlePostSerializer
        return serializers.TitleSerializer


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(Genre, slug=kwargs['pk'])
        if request.user.is_admin or request.user.is_superuser:
            genre.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, permissions.IsAdminUserOrReadOnly)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs['pk'])
        if request.user.is_admin or request.user.is_superuser:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, permissions.IsAuthorOrModer)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.review.all().order_by('id')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        return serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=title_id)
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.AuthorOrHasRoleOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all().order_by('id')

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=review_id)
        )


class SignupView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)

        self.send_confirmation_code(request, user)
        return Response(serializer.data)

    def send_confirmation_code(self, request, username):
        email = request.data.get('email')
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Confirmation code',
            f'{confirmation_code}',
            f'{settings.ADMIN_EMAIL}',
            [f'{email}'],
            fail_silently=False,
        )


class ConfirmationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        confirmation_code = request.data.get('confirmation_code')
        username = request.data.get('username')
        serializer = serializers.ConfirmationCodeSerializer(
            data=self.request.data
        )
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(
            user, confirmation_code
        ):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'confirmation_code is uncorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = serializers.CustomUserSerializer
    permission_classes = (permissions.IsAdminOrSuperuser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = serializers.CustomUserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        user = get_object_or_404(User, username=self.request.user)
        serializer = serializers.CustomUserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data)

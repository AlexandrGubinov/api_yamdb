from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Category(models.Model):
    """Модель категории произведения"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=500)  # Возможно нужно убрать ограничение по символам
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ManyToManyField(Genre, through='TitleGenre')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Моедель для связи ManyToMany"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Rating(models.Model):
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rewiew'
    )
    text = models.TextField()
    score = models.ForeignKey(
        Rating,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text

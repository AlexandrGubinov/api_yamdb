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
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def update_rating(self):
        reviews = self.review.all()
        if reviews.count() > 0:
            ratings_sum = sum(review.score for review in reviews)
            self.rating = round(ratings_sum / reviews.count(), 1)
        else:
            self.rating = None
        self.save()


class TitleGenre(models.Model):
    """Моедель для связи ManyToMany"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


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
    score = models.PositiveIntegerField()
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

#    class Meta:
#        ordering = ['-id']

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]


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
        auto_now_add=True
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text

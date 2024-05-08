from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    date_birth = models.DateField(null=True, blank=True)
    date_death = models.DateField(null=True, blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=100)

class Text(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1 - Начальный'),
        ('A2', 'A2 - Элементарный'),
        ('B1', 'B1 - Средний'),
        ('B2', 'B2 - Выше среднего'),
        ('C1', 'C1 - Продвинутый'),
        ('C2', 'C2 - В совершенстве'),
    ]
    TYPE_CHOICES = [
        ('book', 'Книга'),
        ('news', 'Новость'),
        ('wiki', 'Статья'),
        ('lyrics', 'Текст песни'),
    ]
    LANG_CHOICES = [
        ('RU', 'Русский язык'),
        ('PL', 'Польский язык'),
    ]
    title = models.CharField(max_length=100)
    text_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
    source = models.CharField(max_length=100, null=True, blank=True)
    year = models.SmallIntegerField(null=True, blank=True)
    pages = models.SmallIntegerField(null=True, blank=True)
    time_to_read = models.SmallIntegerField(null=True, blank=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, null=True, blank=True)
    language = models.CharField(max_length=2, choices=LANG_CHOICES, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='text_files/', null=True, blank=True)

class TextEditionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    edited_on = models.DateTimeField(auto_now_add=True)
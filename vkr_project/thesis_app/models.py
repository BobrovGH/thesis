from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    date_birth = models.DateField(null=True, blank=True)
    date_death = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

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
    file = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.title

class TextEditionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    edited_on = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} - {self.edited_on}"
    
class TranslatedSentence(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    paragraph = models.IntegerField()
    sentence_original = models.TextField()
    sentence_translated = models.TextField()

class TranslatedToken(models.Model):
    sentence = models.ForeignKey(TranslatedSentence, on_delete=models.CASCADE)
    word_original = models.CharField(max_length=100)
    word_translated = models.CharField(max_length=100, null=True, blank=True)
    original_token_index = models.IntegerField(null=True, blank=True)
    translated_token_index = models.IntegerField(null=True, blank=True)

class WordOfDictionary(models.Model):
    translated_token = models.ForeignKey(TranslatedToken, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
from django.core.management.base import BaseCommand
from thesis_app.models import TranslatedToken

class Command(BaseCommand):
    help = 'Добавить новый объект в TranslatedToken'

    def handle(self, *args, **kwargs):
        word_original = input("Введите слово на языке оригинала: ")
        word_translated = input("Введите слово на языке перевода: ")
        original_token_index = int(input("Введите индекс для оригинального: "))
        translated_token_index = int(input("Введите индекс для переведённого: "))
        sentence_id = int(input("Введите ID предложения: "))

        data = {
        'word_original': word_original,
        'word_translated': word_translated,
        'original_token_index': original_token_index,
        'translated_token_index': translated_token_index,
        'sentence_id': sentence_id
        }
        # Django ORM добавляет объект и уведомляет об успехе
        translated_token = TranslatedToken.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('Добавлен новый объект в TranslatedToken'))
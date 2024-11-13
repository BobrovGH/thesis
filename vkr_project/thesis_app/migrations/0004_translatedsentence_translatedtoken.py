# Generated by Django 5.0.6 on 2024-05-17 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thesis_app', '0003_texteditionhistory_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslatedSentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paragraph', models.IntegerField()),
                ('sentence_original', models.TextField()),
                ('sentence_translated', models.TextField()),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thesis_app.text')),
            ],
        ),
        migrations.CreateModel(
            name='TranslatedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_original', models.CharField(max_length=100)),
                ('word_translated', models.CharField(max_length=100)),
                ('original_token_index', models.IntegerField(blank=True, null=True)),
                ('translated_token_index', models.IntegerField(blank=True, null=True)),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thesis_app.translatedsentence')),
            ],
        ),
    ]

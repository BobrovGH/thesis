# Generated by Django 5.0.6 on 2024-05-08 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thesis_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='text_files/'),
        ),
    ]

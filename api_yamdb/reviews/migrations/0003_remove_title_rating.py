# Generated by Django 3.2 on 2023-04-10 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_title_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]

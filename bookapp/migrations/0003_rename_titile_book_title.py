# Generated by Django 3.2 on 2025-02-22 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0002_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='titile',
            new_name='title',
        ),
    ]

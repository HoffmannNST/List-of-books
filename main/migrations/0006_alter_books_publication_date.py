# Generated by Django 3.2.6 on 2021-12-09 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_isbn_nr_books_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='publication_date',
            field=models.DateField(max_length=30),
        ),
    ]

# Generated by Django 3.2.6 on 2021-12-02 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='liczba_stron',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

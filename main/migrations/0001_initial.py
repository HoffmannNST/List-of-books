# Generated by Django 3.2.6 on 2021-12-02 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tytul', models.CharField(max_length=200)),
                ('autor', models.CharField(max_length=200)),
                ('data_publikacji', models.DateField(max_length=200)),
                ('numer_isbn', models.CharField(max_length=30)),
                ('link_do_okladki', models.URLField()),
                ('jezyk_publikacji', models.CharField(max_length=40)),
            ],
        ),
    ]
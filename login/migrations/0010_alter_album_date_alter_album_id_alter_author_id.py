# Generated by Django 4.0.1 on 2022-05-10 00:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_author_found_alter_album_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 10, 0, 4, 57, 772330, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
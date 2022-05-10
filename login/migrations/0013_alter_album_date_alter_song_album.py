# Generated by Django 4.0.1 on 2022-05-10 00:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_alter_album_date_alter_song_author_alter_song_feats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 10, 0, 24, 9, 431416, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ManyToManyField(blank=True, to='login.Album'),
        ),
    ]

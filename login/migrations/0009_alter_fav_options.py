# Generated by Django 4.0.1 on 2022-05-10 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_remove_song_album_song_album_remove_song_author_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fav',
            options={'ordering': ['date']},
        ),
    ]

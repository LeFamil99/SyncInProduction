# Generated by Django 4.0.1 on 2022-05-10 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_remove_profile_favs_remove_song_favs_fav_song_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fav',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

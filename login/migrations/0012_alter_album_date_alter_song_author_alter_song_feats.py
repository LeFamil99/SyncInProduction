# Generated by Django 4.0.1 on 2022-05-10 00:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_alter_album_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 10, 0, 18, 32, 878952, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='author',
            field=models.ManyToManyField(blank=True, related_name='written_by', to='login.Author'),
        ),
        migrations.AlterField(
            model_name='song',
            name='feats',
            field=models.ManyToManyField(blank=True, related_name='feat_by', to='login.Author'),
        ),
    ]

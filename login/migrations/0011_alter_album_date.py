# Generated by Django 4.0.1 on 2022-05-10 00:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_album_date_alter_album_id_alter_author_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 10, 0, 5, 9, 514405, tzinfo=utc), null=True),
        ),
    ]
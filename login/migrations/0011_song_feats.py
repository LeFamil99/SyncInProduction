# Generated by Django 4.0.1 on 2022-05-10 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_fav_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='feats',
            field=models.ManyToManyField(blank=True, related_name='feat_by', to='login.Author'),
        ),
    ]

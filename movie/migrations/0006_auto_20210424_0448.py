# Generated by Django 3.1.7 on 2021-04-24 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_auto_20210424_0303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movietags',
            old_name='movie_id',
            new_name='movie',
        ),
        migrations.RenameField(
            model_name='movietags',
            old_name='user_id',
            new_name='user',
        ),
    ]
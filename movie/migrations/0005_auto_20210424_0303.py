# Generated by Django 3.1.7 on 2021-04-24 03:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0004_movietags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movietags',
            old_name='movieid',
            new_name='movie_id',
        ),
        migrations.RemoveField(
            model_name='movietags',
            name='username',
        ),
        migrations.AddField(
            model_name='movietags',
            name='user_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]

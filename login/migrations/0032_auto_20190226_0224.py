# Generated by Django 2.1 on 2019-02-26 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0031_task_user_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_tasks',
            field=models.ManyToManyField(to='login.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='users',
            field=models.ManyToManyField(related_name='claimed_tasks', through='login.TaskUser', to='login.User'),
        ),
    ]

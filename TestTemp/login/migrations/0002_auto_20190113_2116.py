# Generated by Django 2.0.8 on 2019-01-13 13:16

from django.db import migrations, models
import django.db.models.deletion
import login.models


class Migration(migrations.Migration):
    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField(max_length=1024)),
                ('m_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=256, upload_to=login.models.img_directory_path)),
                ('result', models.TextField(max_length=1024)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='content',
            field=models.TextField(default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='task',
            name='template',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='tasks_created', to='login.User'),
        ),
        migrations.AlterField(
            model_name='task',
            name='c_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='task',
            name='users',
            field=models.ManyToManyField(related_name='tasks_owned', to='login.User'),
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.AddField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login.Task'),
        ),
        migrations.AddField(
            model_name='label',
            name='sub_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.SubTask'),
        ),
        migrations.AddField(
            model_name='label',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.User'),
        ),
    ]

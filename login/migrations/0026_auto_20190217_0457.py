# Generated by Django 2.1 on 2019-02-17 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0025_screenshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenshot',
            name='image',
            field=models.FilePathField(max_length=256, path='D:\\Projects\\Pycharm\\login\\media'),
        ),
    ]

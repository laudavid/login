# login/models.py

from django.db import models


class CommonInfo(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        abstract = True


class User(CommonInfo):
    """用户表"""
    pass


class Admin(CommonInfo):
    """管理员表"""
    pass


class Task(models.Model):
    admin = models.ForeignKey('Admin', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ManyToManyField('User')
    name = models.CharField(max_length=128, unique=True)

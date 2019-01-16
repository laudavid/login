# login/models.py
from django.db import models
import hashlib


def gen_md5(s, salt='9527'):  # 加盐
    s += salt
    md5 = hashlib.md5()
    md5.update(s.encode(encoding='utf-8'))  # update方法只接收bytes类型
    return md5.hexdigest()


def img_directory_path(instance, filename):
    # 文件上传到MEDIA_ROOT/task_<id>/<filename>目录中
    return 'task_{0}/{1}'.format(instance.task.id, filename)


def get_untagged_sub_task(task, user):
    label = task.label_set.filter(user=user, is_tagged=False).first()
    if label is not None:
        return label.sub_task
    else:
        return None


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)  # 保存创建时间，不可修改

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["c_time"]


class Task(models.Model):
    """任务表"""

    template = models.IntegerField(default=1)
    content = models.TextField(max_length=1024)  # 针对模板1，保存问题及选项，中以分隔符分隔
    name = models.CharField(max_length=128)
    admin = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='tasks_created')
    users = models.ManyToManyField('User', related_name='tasks_owned')
    details = models.TextField(max_length=1024)
    c_time = models.DateTimeField(auto_now=True)  # 保存最后标记时间，可以修改

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["c_time"]


class SubTask(models.Model):
    """子任务表"""

    image = models.ImageField(max_length=256, upload_to=img_directory_path)
    task = models.ForeignKey('Task', null=True, on_delete=models.CASCADE)
    result = models.TextField(max_length=1024)  # 保存最终标记结果


class Label(models.Model):
    """标签表"""

    task = models.ForeignKey('Task', null=True, on_delete=models.CASCADE)
    sub_task = models.ForeignKey('SubTask', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    result = models.TextField(max_length=1024)  # 保存标记结果
    m_time = models.DateTimeField(auto_now=True)  # 保存最后标记时间
    is_tagged = models.BooleanField(default=False)

# login/views.py
import hashlib
import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from login import forms
from login import models


def gen_md5(s, salt='login'):  # 加盐
    s += salt
    md5 = hashlib.md5()
    md5.update(s.encode(encoding='utf-8'))  # update方法只接收bytes类型
    return md5.hexdigest()


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login', None):
        messages.warning(request, "请勿重复登录！")
        return redirect("/index/")

    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if not login_form.is_valid():
            messages.error(request, "表单信息有误！")
            render(request, 'login.html', locals())

        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']

        if not models.User.objects.filter(name=username).exists():
            messages.error(request, "用户名未注册！")
            return render(request, 'login.html', locals())
        user = models.User.objects.get(name=username)
        if user.password != gen_md5(password, username):
            messages.error(request, "密码错误！")
            return render(request, 'login.html', locals())

        request.session['is_login'] = True
        #  request.session['is_admin'] = user.is_admin
        request.session['is_admin'] = True
        request.session['username'] = username
        messages.success(request, "登录成功！")
        request.session.set_expiry(3600)
        return redirect('/index/')

    login_form = forms.LoginForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        messages.warning(request, "请先退出后再注册！")
        return redirect("/index/")

    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        if not register_form.is_valid():
            messages.error(request, "表单信息有误！")
            return render(request, 'regist.html', locals())

        username = register_form.cleaned_data['username']
        password1 = register_form.cleaned_data['password1']
        password2 = register_form.cleaned_data['password2']
        email = register_form.cleaned_data['email']

        if password1 != password2:  # 两次密码是否相同
            messages.error(request, "两次输入的密码不一致！")
            return render(request, 'regist.html', locals())
        if models.User.objects.filter(name=username).exists():  # 用户名是否唯一
            messages.error(request, "该用户名已注册！")
            return render(request, 'regist.html', locals())
        if models.User.objects.filter(email=email).exists():  # 邮箱地址是否唯一
            messages.error(request, "该邮箱已注册！")
            return render(request, 'regist.html', locals())

        new_user = models.User.objects.create()
        new_user.name = username
        new_user.password = gen_md5(password1, username)
        new_user.email = email
        new_user.is_admin = False  # 只能注册普通用户
        new_user.save()
        print(new_user.c_time)
        messages.success(request, "注册成功！")
        return redirect('/login/')

    register_form = forms.RegisterForm()
    return render(request, 'regist.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        messages.warning(request, "您尚未登录！")
        return redirect("/index/")

    request.session.flush()
    messages.success(request, "退出成功！")
    return redirect("/index/")


def release_task(request):
    # if not request.session.get('is_admin', None):
    #   messages.warning(request, "您没有权限查看该页面！")
    #   return redirect("/index/")
    request.session['new_task_id'] = None
    if request.method == "POST":

        if 'template' in request.POST:
            if request.session.get('new_task_id', None):
                new_task = models.Task.objects.get(id=request.session['new_task_id'])
            else:
                new_task = models.Task.objects.create()
                new_task.admin = models.User.objects.get(name=request.session['username'])
                new_task.save()
                request.session['new_task_id'] = new_task.id
            if request.POST.get('template') == '1':
                new_task.template = 1
                new_task.save()
                return redirect("/release_task/")
            elif request.POST.get('template') == '2':
                new_task.template = 2
                new_task.save()
                return redirect("/release_task/")
            elif request.POST.get('template') == '3':
                new_task.template = 3
                new_task.save()
                return redirect("/release_task/")
        if 'task_name' in request.POST:
            task_form3 = forms.TaskForm3(request.POST)
            if not task_form3.is_valid():
                messages.error(request, "表单信息有误！")
                return render(request, 'release_task.html', locals())
    task_form1 = forms.TaskForm1()
    task_form2 = forms.TaskForm2()
    task_form3 = forms.TaskForm3()
    return render(request, 'release_task.html', locals())


def task(request):
    if not request.session.get('is_login', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    return render(request, 'login/task.html', locals())


def add_task(request):
    if not request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    if request.method == "POST":
        pass
        # task_form = forms.TaskForm(request.POST)
        # if not task_form.is_valid():
        #     messages.error(request, "表单信息有误，请重新填写！")
        #     return render(request, 'login/add_task.html', locals())
        #
        # name = task_form.cleaned_data['name']
        # users_list = task_form.cleaned_data['users']
        # details = task_form.cleaned_data['details']
        #
        # if models.Task.objects.filter(name=name).exists():
        #     messages.error(request, "该任务已存在！")
        #     return render(request, 'login/add_task.html', locals())
        #
        # new_task = models.Task.objects.create()
        # new_task.name = name
        # new_task.details = details
        # new_task.admin = models.Admin.objects.get(name=request.session.get('username', None))
        # new_task.save()
        # for user in users_list:
        #     new_task.users.add(models.User.objects.get(name=user))
        #
        # messages.success(request, "任务发布成功！")
        # return redirect('/task/')

    task_form1 = forms.TaskForm1()
    task_form2 = forms.TaskForm2()
    task_form3 = forms.TaskForm3()
    return render(request, 'login/add_task.html', locals())


def get_all_tasks(request):
    if not request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    search = request.GET.get('search')
    sort_column = request.GET.get('sort')
    order = request.GET.get('order')

    if search:
        all_records = models.Task.objects.filter(name__contains=search)
    else:
        all_records = models.Task.objects.all()

    if sort_column:
        sort_column = sort_column.replace('task_', '')
        if sort_column in ['name', 'admin', 'c_time']:
            if order == 'desc':
                sort_column = '-%s' % sort_column
            all_records = all_records.order_by(sort_column)

    if not offset:
        offset = 0
    if not limit:
        limit = 10

    paginator = Paginator(all_records, limit)
    page = int(int(offset) / int(limit) + 1)
    response_data = {'total': all_records.count(), 'rows': []}

    for per_task in paginator.page(page):
        users_list = []
        for user in per_task.users.all():
            users_list.append(user.name)
        response_data['rows'].append({
            'task_name': per_task.name if per_task.name else '',
            'task_admin': per_task.admin.name if per_task.admin else '',
            'task_users': users_list if per_task.users else '',
            'task_c_time': timezone.localtime(per_task.c_time).ctime() if per_task.c_time else '',
            'task_details': per_task.details if per_task.details else '',
        })

    return HttpResponse(json.dumps(response_data))


def get_user_tasks(request):
    if not request.session.get('is_login', None) or request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    search = request.GET.get('search')
    sort_column = request.GET.get('sort')
    order = request.GET.get('order')

    current_user = models.User.objects.get(name=request.session.get('username', None))

    if search:
        all_records = current_user.tasks_owned.filter(name__contains=search)
    else:
        all_records = current_user.tasks_owned.all()

    if sort_column:
        sort_column = sort_column.replace('task_', '')
        if sort_column in ['name', 'admin', 'c_time']:
            if order == 'desc':
                sort_column = '-%s' % sort_column
            all_records = all_records.order_by(sort_column)

    if not offset:
        offset = 0
    if not limit:
        limit = 10

    paginator = Paginator(all_records, limit)
    page = int(int(offset) / int(limit) + 1)
    response_data = {'total': all_records.count(), 'rows': []}
    for per_task in paginator.page(page):
        response_data['rows'].append({
            'task_name': per_task.name if per_task.name else '',
            'task_admin': per_task.admin.name if per_task.admin.name else '',
            'task_c_time': timezone.localtime(per_task.c_time).ctime() if per_task.c_time else '',
            'task_details': per_task.details if per_task.details else '',
        })

    return HttpResponse(json.dumps(response_data))


def addtask_select_templete(request):
    if not request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    if request.method == "POST":
        if request.session.get('new_task_id', None):
            new_task = models.Task.objects.get(id=request.session['new_task_id'])
        else:
            new_task = models.Task.objects.create()
            new_task.content = '|&&'
            new_task.admin = models.User.objects.get(name=request.session['username'])
            new_task.save()
            request.session['new_task_id'] = new_task.id

        if request.POST.get('template') == '1':
            new_task.template = 1
            new_task.save()
            return redirect("/addtask_step2/")
        if request.POST.get('template') == '2':
            pass
        if request.POST.get('template') == '3':
            pass

    return render(request, 'login/addtask_select_templete.html', locals())


def addtask_set_qa(request):
    if not request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")
    if not request.session.get('new_task_id', None):
        return redirect("/addtask_step1/")

    # task_form2 = forms.TaskForm2()
    if request.method == "POST":
        task_form2 = forms.TaskForm2(request.POST, request.FILES)
        if not task_form2.is_valid():
            messages.error(request, "表单信息有误！")
            return render(request, 'login/addtask_set_qa.html', locals())
        i = 1
        content = ''
        while 'q' + str(i) in request.POST:
            content += '|' + request.POST.get('q' + str(i))
            j = 1
            while 'a' + str(j) + '_q' + str(i) in request.POST:
                content += '&' + request.POST.get('a' + str(j) + '_q' + str(i))
                j += 1
            i += 1
        new_task = models.Task.objects.get(id=request.session['new_task_id'])
        new_task.content = content
        new_task.save()
        img_files = request.FILES.getlist('image')
        if img_files:
            sub_tasks = new_task.subtask_set.all().delete()
            for f in img_files:
                sub_task = models.SubTask.objects.create()
                sub_task.image = f
                sub_task.task = new_task
                sub_task.save()
        if 'last' in request.POST:
            return redirect('/addtask_step1/')
        if 'next' in request.POST:
            return redirect('/addtask_step3/')

    new_task = models.Task.objects.get(id=request.session['new_task_id'])
    qa_list = []
    contents = new_task.content.split('|')
    for item in contents[1:]:
        qa = item.split('&')
        qa_list.append({'question': qa[0], 'answers': qa[1:]})
    img_files = []
    sub_tasks = new_task.subtask_set.all()
    for sub_task in sub_tasks:
        img_file = sub_task.image.name
        img_files.append(img_file)
    task_form2 = forms.TaskForm2()
    return render(request, 'login/addtask_set_qa.html', locals())


def addtask_set_title(request):
    if not request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")
    if not request.session.get('new_task_id', None):
        return redirect("/addtask_step1/")

    if request.method == "POST":
        task_form3 = forms.TaskForm3(request.POST)
        if not task_form3.is_valid():
            messages.error(request, "表单信息有误！")
            return render(request, 'login/addtask_set_title.html', locals())
        name = task_form3.cleaned_data['name']
        new_task = models.Task.objects.get(id=request.session['new_task_id'])
        if models.Task.objects.filter(name=name).exclude(id=request.session['new_task_id']).exists():
            messages.error(request, "该任务名已存在！")
            return render(request, 'login/addtask_set_title.html', locals())
        new_task.name = name
        new_task.save()
        if 'last' in request.POST:
            return redirect('/addtask_step2/')
        if 'next' in request.POST:
            return redirect('/addtask_step4/')

    new_task = models.Task.objects.get(id=request.session['new_task_id'])
    task_form3 = forms.TaskForm3({'name': new_task.name})
    return render(request, 'login/addtask_set_title.html', locals())


def addtask_select_member(request):
    if not request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")
    if not request.session.get('new_task_id', None):
        return redirect("/addtask_step1/")

    if request.method == "POST":
        task_form4 = forms.TaskForm4(request.POST)
        if not task_form4.is_valid():
            messages.error(request, "表单信息有误！")
            return render(request, 'login/addtask_select_member.html', locals())
        new_task = models.Task.objects.get(id=request.session['new_task_id'])
        users = task_form4.cleaned_data['users']
        new_task.users.set(users)
        new_task.save()
        if 'last' in request.POST:
            return redirect('/addtask_step3/')
        if 'next' in request.POST:
            return redirect('/addtask_step5/')

    new_task = models.Task.objects.get(id=request.session['new_task_id'])
    task_form4 = forms.TaskForm4({'users': new_task.users.all()})
    return render(request, 'login/addtask_select_member.html', locals())


def addtask_setdetail(request):
    if not request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")
    if not request.session.get('new_task_id', None):
        return redirect("/addtask_step1/")

    if request.method == "POST":
        task_form5 = forms.TaskForm5(request.POST)
        if not task_form5.is_valid():
            messages.error(request, "表单信息有误！")
            return render(request, 'login/addtask_select_member.html', locals())
        new_task = models.Task.objects.get(id=request.session['new_task_id'])
        details = task_form5.cleaned_data['details']
        new_task.details = details
        new_task.save()
        if 'last' in request.POST:
            return redirect('/addtask_step4/')
        if 'next' in request.POST:
            return redirect('/addtask_step6/')

    new_task = models.Task.objects.get(id=request.session['new_task_id'])
    task_form5 = forms.TaskForm5({'details': new_task.details})
    return render(request, 'login/addtask_setdetail.html', locals())


def addtask_finished(request):
    if not request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")
    if not request.session.get('new_task_id', None):
        return redirect("/addtask_step1/")

    if request.method == "POST":
        if 'last' in request.POST:
            return redirect('/addtask_step5/')
        if 'mytask' in request.POST:
            del request.session['new_task_id']
            return redirect("/task/")
    return render(request, 'login/addtask_finished.html', locals())

from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from app.settings import PER_PAGE
from .models import *
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import NewUserForm, LoginForm, ProfileForm


# Create your views here.

def index(request):
    paginator = Paginator(blog_model.objects.all(), PER_PAGE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'title': 'realcoolsite',
               'data': page_obj}
    return render(request, 'university/index.html', context)


@login_required(login_url='login')
def profile(request):
    instance = request.user.student_model
    group = instance.group

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect("profile")

        messages.error(request, form.errors)

    form = ProfileForm(instance=instance)

    date_start = datetime.now()
    date_end = datetime.now() + timedelta(days=7)
    schedule_data = schedule_model.objects.filter(date__gte=date_start, date__lte=date_end, group=group)

    context = {'title': 'Личный кабинет',
               'form': form, 'data': schedule_data}
    return render(request, 'university/profile.html', context)


def blog_detail(request, slug):
    blog_data = get_object_or_404(blog_model, slug=slug)

    context = {'title': 'realcoolsite',
               'data': blog_data}

    return render(request, 'university/blog_detail.html', context)


def schedule(request):
    date_start = datetime.now()
    date_end = datetime.now() + timedelta(days=7)
    schedule_data = schedule_model.objects.filter(date__gte=date_start, date__lte=date_end).all()

    group_data = group_model.objects.all()

    filter_args = request.GET.get('filter')
    filters = [{'name': "Все", 'is_active': True if not filter_args or filter_args == 'Все' else False}]

    try:
        group_data.get(name=filter_args)
        schedule_data = schedule_data.filter(group__name=filter_args)
    except:
        filter_args = None
        filters[0]['is_active'] = True

    filters += [{'name': i.name, 'is_active': True if filter_args and filter_args == i.name else False}
                for i in group_data]

    ##dobriy den

    context = {'title': 'Расписание',
               'data': schedule_data,
               'filters': filters,
               'date_start': date_start,
               'date_end': date_end, }

    return render(request, 'university/schedule.html', context)


def teachers(request):
    paginator = Paginator(teacher_model.objects.all(), PER_PAGE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'title': 'Преподаватели',
               'data': page_obj}

    return render(request, 'university/teachers.html', context)


def teacher(request, teacher_slug):
    teacher_data = get_object_or_404(teacher_model, slug=teacher_slug)

    context = {'title': f'Преподаватели | {teacher_data.fullname}',
               'data': teacher_data}
    return render(request, 'university/teacher.html', context)


def login_view(request):
    if request.user.is_authenticated: return redirect("index")

    context = {'title': 'Войти', "form": LoginForm()}

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            if user := form.login():
                login(request, user)
                if user.is_superuser or user.is_staff: return redirect('/admin')
                return redirect("index")

        messages.error(request, "Неверный логин или пароль")

    return render(request, "university/login.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def register_request(request):
    if request.user.is_authenticated: return redirect("index")

    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            student = student_model(user=user)
            student.save()
            login(request, user)
            return redirect("profile")
        messages.error(request, form.errors)
    form = NewUserForm()

    context = {'title': 'Войти',
               "register_form": form}
    return render(request, "university/register.html", context)

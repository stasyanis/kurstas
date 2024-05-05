from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField
from django.utils.text import slugify


# Create your models here.
class blog_model(models.Model):
    date = models.DateTimeField(default=datetime.now)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    body = models.TextField(blank=False)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self): return self.title

    class Meta: ordering = ["-date"]


class teacher_model(models.Model):
    image = models.ImageField(upload_to='uploads', blank=True)

    fullname = models.CharField(max_length=150, blank=False)
    job = models.CharField(max_length=200, blank=False)
    short_description = models.CharField(max_length=100, blank=True)
    head_text = models.TextField(blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self): return self.fullname

    class Meta: ordering = ["fullname"]


class group_model(models.Model):
    name = models.CharField(max_length=50)
    institute = models.CharField(max_length=50)

    def __str__(self): return self.name


class subject_model(models.Model):
    subject = models.CharField(max_length=100)

    def __str__(self): return self.subject


class schedule_model(models.Model):
    date = models.DateField(blank=False)
    group = models.ForeignKey(group_model, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(subject_model, through='schedule_subject_model')

    def __str__(self): return f'{self.date} ({self.group})'

    class Meta: ordering = ["date", "group"]


class schedule_subject_model(models.Model):
    schedule = models.ForeignKey(schedule_model, on_delete=models.CASCADE)
    subject = models.ForeignKey(subject_model, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)


class student_model(models.Model):
    user = OneToOneField(User, on_delete = models.CASCADE)
    last_name = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=100, default='')
    patronymic = models.CharField(max_length=100, default='')

    group = models.ForeignKey(group_model, on_delete=models.CASCADE, blank=True, null=True)

    birthday = models.DateField(default=f'{(datetime.now() - timedelta(days=365*16)).date()}')

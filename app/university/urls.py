from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("blog/<slug:slug>", views.blog_detail, name="blog_detail"),
    path("schedule/", views.schedule, name="schedule"),
    path("teachers/", views.teachers, name="teachers"),
    path("teachers/<slug:teacher_slug>", views.teacher, name="teacher"),
    path("profile/", views.profile, name="profile"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register_request, name="register"),
    path("logout/", views.logout_view, name="logout"),
]

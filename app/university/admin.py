from django.contrib import admin

from university.models import *


# Register your models here.

@admin.register(blog_model)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['date', 'title', 'author', 'slug']
    list_filter = ['date', 'author']

    prepopulated_fields = {'slug': ('title',)}


@admin.register(teacher_model)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'job', 'slug']
    list_display_links = ('fullname', 'slug')

    list_filter = ['job']
    sortable_by = ['fullname', 'job']
    search_fields = ("fullname",)

    prepopulated_fields = {'slug': ('fullname',)}


@admin.register(group_model)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'institute']
    list_filter = ['institute']


class ScheduleSubjectsInlineAdmin(admin.StackedInline):
    model = schedule_subject_model
    extra = 0


@admin.register(subject_model)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ("subject",)


@admin.register(schedule_model)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['date', 'group']
    list_filter = ['date', 'group']

    inlines = [ScheduleSubjectsInlineAdmin]


@admin.register(student_model)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_fullname', 'group']
    list_filter = ['group']

    def get_fullname(self, obj): return f'{obj.last_name} {obj.first_name} {obj.patronymic}'

    get_fullname.short_description = "Fullname"

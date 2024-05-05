# Generated by Django 5.0 on 2024-02-18 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0005_student_model_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_model',
            name='birthday',
            field=models.DateField(default='1970-01-01'),
        ),
        migrations.AlterField(
            model_name='student_model',
            name='first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='student_model',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='student_model',
            name='patronymic',
            field=models.CharField(default='', max_length=100),
        ),
    ]

# Generated by Django 5.0 on 2024-02-18 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0007_alter_student_model_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_model',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='university.group_model'),
        ),
    ]

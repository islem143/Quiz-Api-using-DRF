# Generated by Django 3.2.7 on 2021-12-16 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_api', '0007_rename_desciption_exam_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
    ]

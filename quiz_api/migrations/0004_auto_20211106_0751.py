# Generated by Django 3.2.7 on 2021-11-06 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_api', '0003_alter_question_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_exam_choices',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz_api.question'),
        ),
        migrations.AlterUniqueTogether(
            name='student_exam_choices',
            unique_together={('student_exam', 'choice', 'question')},
        ),
    ]
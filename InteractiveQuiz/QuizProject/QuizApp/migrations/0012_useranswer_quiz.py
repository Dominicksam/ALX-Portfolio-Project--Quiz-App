# Generated by Django 4.1.1 on 2024-09-24 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0011_useranswer_delete_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='quiz',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='QuizApp.quiz'),
        ),
    ]

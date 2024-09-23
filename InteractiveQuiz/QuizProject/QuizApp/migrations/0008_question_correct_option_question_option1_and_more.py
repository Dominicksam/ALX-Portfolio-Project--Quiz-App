# Generated by Django 4.1.1 on 2024-09-23 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0007_remove_question_correct_option_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct_option',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='option1',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='option2',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='option3',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='option4',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(default='Question', max_length=255),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='New Quiz', max_length=200),
        ),
    ]

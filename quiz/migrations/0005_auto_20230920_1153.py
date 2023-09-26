# Generated by Django 3.2.20 on 2023-09-20 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_remove_quizquestion_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizquestion',
            name='answers',
        ),
        migrations.AddField(
            model_name='choiceexplanation',
            name='isCorrect',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='choiceexplanation',
            name='choice_text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='choiceexplanation',
            name='explanation_text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='explanation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='question_text',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
# Generated by Django 3.2.20 on 2023-09-19 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceExplanation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=255)),
                ('explanation_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('question_image', models.ImageField(blank=True, null=True, upload_to='question_images/')),
                ('explanation', models.TextField(blank=True, null=True)),
                ('explanation_image', models.ImageField(blank=True, null=True, upload_to='explanation_images/')),
                ('answers', models.ManyToManyField(to='quiz.ChoiceExplanation')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.field')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.subject')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.IntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quizquestion')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.year')),
            ],
        ),
        migrations.AddField(
            model_name='field',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.subject'),
        ),
        migrations.AddField(
            model_name='choiceexplanation',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quizquestion'),
        ),
    ]

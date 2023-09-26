# Generated by Django 3.2.21 on 2023-09-26 15:16

import adminsortable.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_auto_20230926_1055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choiceexplanation',
            options={'ordering': ['the_order']},
        ),
        migrations.AlterModelOptions(
            name='field',
            options={'ordering': ['the_order']},
        ),
        migrations.AlterModelOptions(
            name='questioninstance',
            options={'ordering': ['the_order']},
        ),
        migrations.AlterModelOptions(
            name='quizquestion',
            options={'ordering': ['the_order']},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['the_order']},
        ),
        migrations.AlterModelOptions(
            name='year',
            options={'ordering': ['the_order']},
        ),
        migrations.AddField(
            model_name='choiceexplanation',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='field',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='questioninstance',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='subject',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='year',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='choiceexplanation',
            name='question',
            field=adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quizquestion'),
        ),
        migrations.AlterField(
            model_name='field',
            name='subject',
            field=adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.subject'),
        ),
        migrations.AlterField(
            model_name='questioninstance',
            name='question',
            field=adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quizquestion'),
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='field',
            field=adminsortable.fields.SortableForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='quiz.field'),
            preserve_default=False,
        ),
    ]

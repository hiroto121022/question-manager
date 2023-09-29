from django.db import models
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

class Grade(SortableMixin):
    name = models.CharField(max_length=30)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ["the_order"]

    def __str__(self):
        return self.name

class Subject(SortableMixin):
    grade = SortableForeignKey(Grade, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ["the_order"]

    def __str__(self):
        return self.name

class Field(SortableMixin):
    subject = SortableForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True) # 追加する

    class Meta:
        ordering = ["the_order"]

    def __str__(self):
        return self.name

class Year(SortableMixin):
    year = models.IntegerField(unique=True)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True) # 追加する

    class Meta:
        ordering = ["the_order"]

    def __str__(self):
        return str(self.year)

class QuizQuestion(SortableMixin):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    field = SortableForeignKey(Field, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.CharField(max_length=255)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True) # 追加する

    class Meta:
        ordering = ["the_order"]

    def __str__(self):
        return f"{self.subject}-{self.field}-{self.question_text}"

    question_image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    explanation = models.CharField(max_length=255, null=True, blank=True)
    explanation_image = models.ImageField(upload_to='explanation_images/', null=True, blank=True)

class ChoiceExplanation(SortableMixin):
    question = SortableForeignKey(QuizQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255, null=True, blank=True)
    explanation_text = models.CharField(max_length=255, null=True, blank=True)
    isCorrect = models.BooleanField(default=False)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True) # 追加する

    class Meta:
        ordering = ["the_order"]

    def __str__(self):
        return f"問題:{self.question} 選択肢:{self.choice_text}"

class QuestionInstance(SortableMixin):
    question = SortableForeignKey(QuizQuestion, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True) # 追加する

    class Meta:
        ordering = ["the_order"]

    def __str__(self):
        return f"{self.question.subject}-{self.year}-{self.question_number} - {self.question.question_text}"

class Content(models.Model):
    title = models.CharField(max_length=255)  # レベル1のタイトル
    body = models.TextField()  # レベル1の本文

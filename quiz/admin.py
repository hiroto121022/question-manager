from django.contrib import admin
from .models import Grade, Subject, Field, Year, ChoiceExplanation, QuizQuestion, QuestionInstance
from adminsortable.admin import SortableAdmin

admin.site.register(Grade)
admin.site.register(ChoiceExplanation)
admin.site.register(QuestionInstance)

class YearAdmin(SortableAdmin):
    list_display = ('id', 'year')
    list_display_links = ('id', 'year')

class SubjectAdmin(SortableAdmin):
    list_display = ('id', 'name', 'grade')
    list_display_links = ('id', 'name')

class FieldAdmin(SortableAdmin):
    list_display = ('id', 'name', 'subject')
    list_display_links = ('id', 'name')

class QuizQuestionAdmin(SortableAdmin):
    list_display = ('the_order', 'question_text', 'field', 'explanation')
    list_display_links = ('id', 'question_text', 'field')

admin.site.register(Year, YearAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(QuizQuestion, QuizQuestionAdmin)

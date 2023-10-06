from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import QuizQuestion, ChoiceExplanation, QuestionInstance, Subject, Year, Field

class QuizQuestionForm(forms.ModelForm):

    question_text = forms.CharField(widget=forms.Textarea(attrs={'cols': '70', 'rows': '3'}))
    explanation = forms.CharField(widget=forms.Textarea(attrs={'cols': '70', 'rows': '3'}), required=False)

    class Meta:
        model = QuizQuestion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # subjectフィールドから選択された値を取得
        selected_subject = self.initial.get('subject', None)
        # 関連するFieldのクエリセットをフィルタリングして設定
        self.fields['field'].queryset = Field.objects.filter(subject=selected_subject)

class ChoiceExplanationForm(forms.ModelForm):

    choice_text = forms.CharField(widget=forms.Textarea(attrs={'cols': '70', 'rows': '2'}))
    explanation_text = forms.CharField(widget=forms.Textarea(attrs={'cols': '70', 'rows': '2'}), required=False)

    class Meta:
        model = ChoiceExplanation
        fields = ['choice_text', 'explanation_text', 'isCorrect']

ChoiceExplanationFormSet = formset_factory(ChoiceExplanationForm, extra=5)
ChoiceExplanationFormSet2 = modelformset_factory(ChoiceExplanation, form=ChoiceExplanationForm, extra=0)


class QuestionInstanceForm(forms.ModelForm):
    class Meta:
        model = QuestionInstance
        fields = ['year', 'question_number']

QuestionInstanceFormSet = formset_factory(QuestionInstanceForm, extra=1)
QuestionInstanceFormSet2 = modelformset_factory(QuestionInstance, form=QuestionInstanceForm, extra=0)

class ContentUploadForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label='Subject')
    docx_file = forms.FileField(label='Upload DOCX File')

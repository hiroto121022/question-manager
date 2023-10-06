from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views.generic.edit import UpdateView, CreateView
from .forms import QuizQuestionForm, ContentUploadForm, ChoiceExplanationFormSet, QuestionInstanceFormSet, ChoiceExplanationFormSet2, QuestionInstanceFormSet2
from .models import QuizQuestion, ChoiceExplanation, QuestionInstance, Year, Subject, Field, Content, Grade
from django.http import JsonResponse
from docx import Document as DocxDocument
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
import re

def index(request):
    subjects = Subject.objects.all()
    return render(request, 'index.html', {'subjects': subjects})

def get_years(request):
    years = Year.objects.values('id', 'year')
    return JsonResponse({'years': list(years)})

def subject_list(request):
    grade_3_subjects = Subject.objects.filter(grade_id=1)
    grade_4_subjects = Subject.objects.filter(grade_id=2)
    return render(request, 'subject_list.html', {'grade_3_subjects': grade_3_subjects, 'grade_4_subjects': grade_4_subjects})

def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    fields = Field.objects.filter(subject=subject)
    years = Year.objects.filter(questioninstance__question__subject=subject).distinct()

    return render(request, 'subject_detail.html', {'subject': subject, 'fields': fields, 'years': years})

def field_questions(request, field_id):
    field = get_object_or_404(Field, pk=field_id)
    questions = QuizQuestion.objects.filter(field=field)
    for question in questions:
        question.correct_choices = [chr(i + 97) for i, choice in enumerate(question.choiceexplanation_set.all()) if choice.isCorrect]

    return render(request, 'field_questions.html', {'field': field, 'questions': questions})

def year_questions(request, subject_id, year_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    year = get_object_or_404(Year, pk=year_id)

    # QuestionInstance モデルを介して問題番号を取得
    question_instances = QuestionInstance.objects.filter(year=year, question__subject=subject).order_by('question_number')
    for question_instance in question_instances:
        question_instance.question.correct_choices = [chr(i + 97) for i, choice in enumerate(question_instance.question.choiceexplanation_set.all()) if choice.isCorrect]

    return render(request, 'year_questions.html', {'subject': subject, 'year': year, 'question_instances': question_instances})

def edit_subject_list(request):
    grade_3_subjects = Subject.objects.filter(grade_id=1)
    grade_4_subjects = Subject.objects.filter(grade_id=2)
    return render(request, 'edit_subject_list.html', {'grade_3_subjects': grade_3_subjects, 'grade_4_subjects': grade_4_subjects})

def edit_subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    fields = Field.objects.filter(subject=subject)
    years = Year.objects.filter(questioninstance__question__subject=subject).distinct()

    return render(request, 'edit_subject_detail.html', {'subject': subject, 'fields': fields, 'years': years})

def edit_field_questions(request, field_id):
    field = get_object_or_404(Field, pk=field_id)
    questions = QuizQuestion.objects.filter(field=field)

    return render(request, 'edit_field_questions.html', {'field': field, 'questions': questions})

def edit_year_questions(request, subject_id, year_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    year = get_object_or_404(Year, pk=year_id)

    # QuestionInstance モデルを介して問題番号を取得
    question_instances = QuestionInstance.objects.filter(year=year, question__subject=subject).order_by('question_number')

    return render(request, 'edit_year_questions.html', {'subject': subject, 'year': year, 'question_instances': question_instances})
'''
def create_question(request):
    years = Year.objects.all()

    if request.method == 'POST':
        form = QuizQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            # フォームからクリーンデータを取得
            subject = form.cleaned_data['subject']
            field = form.cleaned_data['field']
            question_text = form.cleaned_data['question_text']
            question_image = form.cleaned_data['question_image']
            explanation = form.cleaned_data['explanation']
            explanation_image = form.cleaned_data['explanation_image']

            # クイズの質問を保存
            quiz_question = QuizQuestion(
                subject=subject,
                field=field,
                question_text=question_text,
                question_image=question_image,
                explanation=explanation,
                explanation_image=explanation_image,
            )
            quiz_question.save()

            # 選択肢セットを保存
            index = 1
            while f'choice_texts_{index}' in request.POST:
                choice_text = request.POST[f'choice_texts_{index}']
                explanation_text = request.POST[f'explanation_texts_{index}']
                is_correct = request.POST[f'is_correct_values_{index}']

                choice = ChoiceExplanation(
                    question=quiz_question,
                    choice_text=choice_text,
                    explanation_text=explanation_text,
                    isCorrect=is_correct
                )
                choice.save()

                index += 1

            # 年・質問番号セットを保存
            index = 1
            while f'years_{index}' in request.POST:
                year_str = request.POST[f'years_{index}']  # 年の文字列を取得
                year_instance = Year.objects.get(year=year_str)  # 文字列からYearモデルのインスタンスを取得
                question_number = request.POST[f'question_numbers_{index}']

                question_instance = QuestionInstance(
                    question=quiz_question,
                    year=year_instance,  # Yearモデルのインスタンスを割り当てる
                    question_number=question_number
                )
                question_instance.save()

                index += 1

            return redirect('create_question')  # データが正常に保存された後のリダイレクト先URLを設定します
    else:
        form = QuizQuestionForm()

    return render(request, 'create_question.html', {'form': form, 'years': years})
'''

class QuizQuestionCreateView(CreateView):
    model = QuizQuestion
    form_class = QuizQuestionForm
    template_name = 'create_question.html'
    success_url = reverse_lazy('create_question')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['choice_formset'] = ChoiceExplanationFormSet(self.request.POST, prefix='choice', extra=5)
            context['question_formset'] = QuestionInstanceFormSet(self.request.POST, prefix='question', extra=1)
        else:
            context['choice_formset'] = ChoiceExplanationFormSet(prefix='choice')
            context['question_formset'] = QuestionInstanceFormSet(prefix='question')
            return context

    def form_valid(self, form):
        # クイズの質問を保存
        quiz_question = form.save()

        # 選択肢セットを保存
        choice_formset = ChoiceExplanationFormSet(self.request.POST, prefix='choice')
        if choice_formset.is_valid():
            for choice_form in choice_formset:
                choice = choice_form.save(commit=False)
                choice.question = quiz_question
                choice.save()

        # 年・質問番号セットを保存
        question_formset = QuestionInstanceFormSet(self.request.POST, prefix='question')
        if question_formset.is_valid():
            for question_form in question_formset:
                question = question_form.save(commit=False)
                question.question = quiz_question
                question.save()

        return super().form_valid(form)

class QuizQuestionUpdateView(UpdateView):
    model = QuizQuestion
    form_class = QuizQuestionForm
    template_name = 'update_question.html'
    success_url = reverse_lazy('field_questions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['choice_formset'] = ChoiceExplanationFormSet2(self.request.POST, prefix='choice')
            context['question_formset'] = QuestionInstanceFormSet2(self.request.POST, prefix='question')
        else:
            context['choice_formset'] = ChoiceExplanationFormSet2(queryset=ChoiceExplanation.objects.filter(question=self.object), prefix='choice')
            context['question_formset'] = QuestionInstanceFormSet2(queryset=QuestionInstance.objects.filter(question=self.object), prefix='question')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        choice_formset = context['choice_formset']
        question_formset = context['question_formset']

        if choice_formset.is_valid() and question_formset.is_valid():
            self.object = form.save()

            choices = choice_formset.save(commit=False)
            for choice in choices:
                choice.question = self.object
                choice.save()

            questions = question_formset.save(commit=False)
            for question in questions:
                question.question = self.object
                question.save()

            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return resolve_url('update_question', self.object.id)

def get_fields(request):
    selected_subject = request.GET.get('subject')
    fields = Field.objects.filter(subject_id=selected_subject).values('id', 'name')
    return JsonResponse({'fields': list(fields)})

def answer_question(request, question_id):
    # 問題情報を取得
    question_pks = request.session.get('question_pks', [])

    if question_id in question_pks:
        # question_idがリストにある場合、その質問を取得
        question = get_object_or_404(QuizQuestion, pk=question_id)
        choices = ChoiceExplanation.objects.filter(question=question).order_by("?")
        correct_choices = [chr(i + 97) for i, choice in enumerate(choices) if choice.isCorrect]

        # 次の質問のpkを取得（存在しない場合はNone）
        if request.method == 'POST':
            # ユーザーが「次の問題へ行く」ボタンをクリックした場合
            if 'next_question' in request.POST:
                # 次の質問のPKを取得
                current_index = question_pks.index(question_id)
                if current_index + 1 < len(question_pks):
                    next_pk = question_pks[current_index + 1]
                    # 次の質問のURLにリダイレクト
                    return redirect('answer_question', question_id=next_pk)
                else:
                    # 最後の質問の場合は指定のページにリダイレクト
                    subject_id = question.subject.id  # subjectのidを取得
                    return redirect('subject_detail', subject_id=subject_id)

        question_pks_count = len(question_pks)
        current_index = question_pks.index(question_id) + 1
        context = {
            'question': question,
            'choices': choices,
            'correct_choices': correct_choices,
            'question_pks_count': question_pks_count,
            'current_index': current_index,
        }

        # コンテキストを正しく渡すために {} の中に変数名を含めて修正
        return render(request, 'answer_question.html', {'context': context})

    else:
        # pkがリストにない場合、エラーページにリダイレクト
        return redirect('error_page')

def extract_and_store_content(request):
    if request.method == 'POST':
        form = ContentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # フォームが有効な場合、ファイルを処理します
            subject = form.cleaned_data['subject']
            docx_file = request.FILES['docx_file']

            doc = DocxDocument(docx_file)

            current_question_text = None
            current_choices = []
            current_years_and_numbers = []
            current_answer_indices = []  # 複数の答えを格納するリスト

            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()

                if paragraph.style.name.startswith("Heading 1"):
                    if current_question_text and current_choices:
                        # QuizQuestionモデルに保存
                        question = QuizQuestion.objects.create(
                            subject=subject,
                            question_text=current_question_text
                        )

                        # ChoiceExplanationモデルに選択肢と説明を保存
                        for index, choice_text in enumerate(current_choices):
                            is_correct = index in current_answer_indices  # 正解選択肢を設定
                            ChoiceExplanation.objects.create(
                                question=question,
                                choice_text=choice_text,
                                isCorrect=is_correct
                            )

                        # QuestionInstanceモデルに関連するデータを保存
                        for year, question_number in current_years_and_numbers:
                            year_instance = Year.objects.get(year=year)
                            QuestionInstance.objects.create(
                                question=question,
                                year=year_instance,
                                question_number=question_number
                            )

                    # レベル1の行から問題文と年度-問題番号情報を取得
                    match = re.search(r'^(.*?)\((.*?)\)$', text)
                    if match:
                        current_question_text = match.group(1).strip()  # 問題文を取得
                        years_and_numbers = match.group(2).split(',')  # 年度-問題番号情報をカンマで分割
                        current_years_and_numbers = [(year.strip(), number.strip()) for year, number in (pair.split('-') for pair in years_and_numbers)]

                    current_choices = []
                    current_answer_indices = []

                elif paragraph.style.name.startswith("Heading 2"):
                    # "レベル2" の行は答えを表します
                    answer_text = text.replace("答.", "").strip()
                    # 複数の答えをカンマで区切って処理
                    current_answer_indices = [ord(answer) - ord('a') for answer in answer_text.split(',') if answer]

                elif text:
                    # 選択肢の行を処理します
                    # 段落の先頭にある a.、b.、c.、d.、e. を取り除いて選択肢のテキストを抽出
                    choice_text = re.sub(r'^[a-eA-E]\.', '', text).strip()
                    current_choices.append(choice_text)

            # ドキュメントの終了時に最後のデータを保存します
            if current_question_text and current_choices:
                question = QuizQuestion.objects.create(
                    subject=subject,
                    question_text=current_question_text
                )

                for index, choice_text in enumerate(current_choices):
                    is_correct = index in current_answer_indices  # 正解選択肢を設定
                    ChoiceExplanation.objects.create(
                        question=question,
                        choice_text=choice_text,
                        isCorrect=is_correct
                    )

                for year, question_number in current_years_and_numbers:
                    year_instance = Year.objects.get(year=year)
                    QuestionInstance.objects.create(
                        question=question,
                        year=year_instance,
                        question_number=question_number
                    )
            return redirect('upload_document')  # 成功ページにリダイレクト
    else:
        form = ContentUploadForm()

    return render(request, 'upload_form.html', {'form': form, 'subjects': Subject.objects.all()})

def start_question(request, subject_id):
    # Get the subject based on subject_id
    subject = get_object_or_404(Subject, pk=subject_id)

    # Get all questions related to the subject (you need to implement this query)
    questions = QuizQuestion.objects.filter(subject=subject)

    if questions.exists():
        # Create a list of question IDs
        question_ids = [question.id for question in questions]
        request.session.clear()
        # Store the question IDs in the session
        request.session['question_pks'] = question_ids

        # Redirect to the first question's answer page
        return redirect('answer_question', question_id=question_ids[0])
    else:
        # Handle the case where there are no questions for the subject
        return redirect('error_page')  # You should define 'error_page' URL

def start_question_field(request, field_id):
    # Get the subject based on subject_id
    field = get_object_or_404(Field, pk=field_id)

    # Get all questions related to the subject (you need to implement this query)
    questions = QuizQuestion.objects.filter(field=field)

    if questions.exists():
        # Create a list of question IDs
        question_ids = [question.id for question in questions]
        request.session.clear()
        request.session['question_pks'] = question_ids
        return redirect('answer_question', question_id=question_ids[0])
    else:
        # Handle the case where there are no questions for the subject
        return redirect('error_page')  # You should define 'error_page' URL

def start_question_year(request, subject_id, year_id):
    # QuestionInstance モデルを介して問題番号を取得
    subject = get_object_or_404(Subject, pk=subject_id)
    year = get_object_or_404(Year, pk=year_id)
    questions = QuizQuestion.objects.filter(questioninstance__year=year, subject=subject).order_by('questioninstance__question_number')

    if questions.exists():
        question_ids = [question.id for question in questions]
        request.session.clear()
        request.session['question_pks'] = question_ids
        return redirect('answer_question', question_id=question_ids[0])
    else:
        return redirect('error_page')

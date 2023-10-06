from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import QuizQuestionCreateView
from .views import QuizQuestionUpdateView

urlpatterns = [
    path('', views.index, name='index'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('fields/<int:field_id>/', views.field_questions, name='field_questions'),
    path('subject/<int:subject_id>/year/<int:year_id>/', views.year_questions, name='year_questions'),
    path('edit_subjects/', views.edit_subject_list, name='edit_subject_list'),
    path('edit_subjects/<int:subject_id>/', views.edit_subject_detail, name='edit_subject_detail'),
    path('edit_fields/<int:field_id>/', views.edit_field_questions, name='edit_field_questions'),
    path('edit_subject/<int:subject_id>/year/<int:year_id>/', views.edit_year_questions, name='edit_year_questions'),
    path('api/fields/', views.get_fields, name='get_fields'),
    path('Answer/<int:question_id>/', views.answer_question, name='answer_question'),
    path('upload/', views.extract_and_store_content, name='upload_document'),
    path('get_years/', views.get_years, name='get_years'),
    path('subject/<int:subject_id>/start_question/', views.start_question, name='start_question'),
    path('field/<int:field_id>/start_question/', views.start_question_field, name='start_question_field'),
    path('subject/<int:subject_id>/year/<int:year_id>/start_question/', views.start_question_year, name='start_question_year'),
    path('create_question/', QuizQuestionCreateView.as_view(), name='create_question'),
    path('update_question/<int:pk>/', QuizQuestionUpdateView.as_view(), name='update_question'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

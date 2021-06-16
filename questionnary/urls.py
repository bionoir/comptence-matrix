from django.urls import path
from django.conf.urls import include
from . import views

app_name = "questionnary"
urlpatterns = [
    path('', views.questionnary_answers_view, name='index'),
    path('about',views.questionnary_about_view, name='about'),
    path('<int:question_id>/detail', views.questionnary_answer_edit, name='edit_answer'),
    path('<int:answer_id>/answer_delete', views.questionnary_answer_delete, name='delete_answer'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', views.questionnary_admin_view, name='admin_index'),
    path('admin/create/', views.questionnary_admin_create_view, name='admin_create'),
]

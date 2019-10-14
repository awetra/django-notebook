from django.urls import path

from . import views


urlpatterns = [
    path('', views.NoteList.as_view(), name='notes_list'),
    path('note/create/', views.NoteCreate.as_view(), name='note_create'),
    path('note/delete/<slug:slug>/', views.NoteDelete.as_view(), name='note_delete'),
    path('note/<slug:slug>/', views.NoteDetail.as_view(), name='note_detail'),
    path('note/<slug:slug>/task-delete/<int:pk>/', views.TaskDelete.as_view(), name='task_delete')
]
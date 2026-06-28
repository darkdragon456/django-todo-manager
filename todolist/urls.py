from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('todolist/', views.todolist, name='todolist'),

    path('delete/<int:task_id>/', views.Delete_task, name='Delete_task'),

    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),

    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),

    path('pending/<int:task_id>/', views.pending_task, name='pending_task'),

    path('contact/', views.contact, name='contact'),

    path('about/', views.about, name='about'),
]
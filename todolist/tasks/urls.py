from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('create/', views.task_create, name='task-create'),
    path('update/<str:pk>/', views.task_update, name='task-update'),
    path('delete/<str:pk>/', views.task_delete, name='task-delete'),
]

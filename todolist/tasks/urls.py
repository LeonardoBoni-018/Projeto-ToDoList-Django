from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/create/', views.task_create, name='task-create'),
    path('tasks/update/<str:pk>/', views.task_update, name='task-update'),
    path('tasks/delete/<str:pk>/', views.task_delete, name='task-delete'),
]

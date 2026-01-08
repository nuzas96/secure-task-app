from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),

    path('admin/', views.admin_task_list, name='admin_task_list'),
    path('edit/<int:task_id>/', views.task_update, name='task_update'),
]

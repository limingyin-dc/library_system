from django.urls import path
from . import views

urlpatterns = [
    path('', views.copy_list, name='copy_list'),
    path('create/', views.copy_create, name='copy_create'),
    path('<int:pk>/edit/', views.copy_edit, name='copy_edit'),
    path('<int:pk>/delete/', views.copy_delete, name='copy_delete'),
]

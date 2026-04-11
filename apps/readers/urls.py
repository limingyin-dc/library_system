from django.urls import path
from . import views

urlpatterns = [
    path('', views.reader_list, name='reader_list'),
    path('create/', views.reader_create, name='reader_create'),
    path('<int:pk>/', views.reader_detail, name='reader_detail'),
    path('<int:pk>/edit/', views.reader_edit, name='reader_edit'),
    path('<int:pk>/delete/', views.reader_delete, name='reader_delete'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchase_list, name='purchase_list'),
    path('create/', views.purchase_create, name='purchase_create'),
    path('<int:pk>/edit/', views.purchase_edit, name='purchase_edit'),
    path('<int:pk>/delete/', views.purchase_delete, name='purchase_delete'),
]

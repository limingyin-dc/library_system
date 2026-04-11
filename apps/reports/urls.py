from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_index, name='report_index'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.borrow_list, name='borrow_list'),
    path('create/', views.borrow_create, name='borrow_create'),
    path('<int:pk>/return/', views.borrow_return, name='borrow_return'),
    # 读者自助
    path('my/', views.my_borrows, name='my_borrows'),
    path('request/', views.borrow_request_create, name='borrow_request_create'),
    path('request/<int:pk>/cancel/', views.borrow_request_cancel, name='borrow_request_cancel'),
    # 馆员审批
    path('requests/', views.borrow_request_list, name='borrow_request_list'),
    path('requests/<int:pk>/approve/', views.borrow_request_approve, name='borrow_request_approve'),
]

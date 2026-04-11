from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import User
from .forms import UserCreateForm, UserEditForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, '用户名或密码错误')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    from apps.books.models import Book
    from apps.readers.models import Reader
    from apps.borrow.models import BorrowRecord
    from apps.purchase.models import PurchaseOrder
    context = {
        'book_count': Book.objects.count(),
        'reader_count': Reader.objects.count(),
        'borrow_count': BorrowRecord.objects.filter(status='borrowed').count(),
        'purchase_count': PurchaseOrder.objects.filter(status='pending').count(),
    }
    return render(request, 'dashboard.html', context)


@login_required
def user_list(request):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def user_create(request):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    form = UserCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, '用户创建成功')
        return redirect('user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': '新增用户'})


@login_required
def user_edit(request, pk):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    form = UserEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, '用户更新成功')
        return redirect('user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': '编辑用户'})


@login_required
def user_delete(request, pk):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, '用户删除成功')
        return redirect('user_list')
    return render(request, 'confirm_delete.html', {'obj': user, 'cancel_url': reverse('user_list')})

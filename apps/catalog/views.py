from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from .models import BookCopy
from .forms import BookCopyForm


@login_required
def copy_list(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    qs = BookCopy.objects.select_related('book').all()
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(book__title__icontains=q) | qs.filter(barcode__icontains=q)
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'catalog/copy_list.html', {'page_obj': page, 'q': q})


@login_required
def copy_create(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('copy_list')
    form = BookCopyForm(request.POST or None)
    if form.is_valid():
        copy = form.save()
        # 更新图书副本数
        book = copy.book
        book.total_copies = book.bookcopy_set.count()
        book.available_copies = book.bookcopy_set.filter(status='available').count()
        book.save()
        messages.success(request, '副本添加成功')
        return redirect('copy_list')
    return render(request, 'catalog/copy_form.html', {'form': form, 'title': '新增副本'})


@login_required
def copy_edit(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('copy_list')
    copy = get_object_or_404(BookCopy, pk=pk)
    form = BookCopyForm(request.POST or None, instance=copy)
    if form.is_valid():
        copy = form.save()
        book = copy.book
        book.total_copies = book.bookcopy_set.count()
        book.available_copies = book.bookcopy_set.filter(status='available').count()
        book.save()
        messages.success(request, '副本更新成功')
        return redirect('copy_list')
    return render(request, 'catalog/copy_form.html', {'form': form, 'title': '编辑副本'})


@login_required
def copy_delete(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('copy_list')
    copy = get_object_or_404(BookCopy, pk=pk)
    if request.method == 'POST':
        book = copy.book
        copy.delete()
        book.total_copies = book.bookcopy_set.count()
        book.available_copies = book.bookcopy_set.filter(status='available').count()
        book.save()
        messages.success(request, '副本删除成功')
        return redirect('copy_list')
    return render(request, 'confirm_delete.html', {'obj': copy, 'cancel_url': reverse('copy_list')})

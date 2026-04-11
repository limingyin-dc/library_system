from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Reader
from .forms import ReaderForm


@login_required
def reader_list(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    qs = Reader.objects.all()
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(card_no__icontains=q)
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'readers/reader_list.html', {'page_obj': page, 'q': q})


@login_required
def reader_create(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('reader_list')
    form = ReaderForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, '读者添加成功')
        return redirect('reader_list')
    return render(request, 'readers/reader_form.html', {'form': form, 'title': '新增读者'})


@login_required
def reader_edit(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('reader_list')
    reader = get_object_or_404(Reader, pk=pk)
    form = ReaderForm(request.POST or None, instance=reader)
    if form.is_valid():
        form.save()
        messages.success(request, '读者信息更新成功')
        return redirect('reader_list')
    return render(request, 'readers/reader_form.html', {'form': form, 'title': '编辑读者'})


@login_required
def reader_delete(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('reader_list')
    reader = get_object_or_404(Reader, pk=pk)
    if request.method == 'POST':
        reader.delete()
        messages.success(request, '读者删除成功')
        return redirect('reader_list')
    return render(request, 'confirm_delete.html', {'obj': reader, 'cancel_url': reverse('reader_list')})


@login_required
def reader_detail(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    reader = get_object_or_404(Reader, pk=pk)
    borrows = reader.borrowrecord_set.select_related('book_copy__book').order_by('-borrow_date')
    return render(request, 'readers/reader_detail.html', {'reader': reader, 'borrows': borrows})

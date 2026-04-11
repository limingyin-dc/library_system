from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Book, Category
from .forms import BookForm, CategoryForm


@login_required
def book_list(request):
    qs = Book.objects.select_related('category').all()
    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    if q:
        qs = qs.filter(title__icontains=q) | qs.filter(author__icontains=q) | qs.filter(isbn__icontains=q)
    if category_id:
        qs = qs.filter(category_id=category_id)
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get('page'))
    categories = Category.objects.all()
    return render(request, 'books/book_list.html', {
        'page_obj': page, 'categories': categories, 'q': q, 'category_id': category_id
    })


@login_required
def book_create(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('book_list')
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, '图书添加成功')
        return redirect('book_list')
    return render(request, 'books/book_form.html', {'form': form, 'title': '新增图书'})


@login_required
def book_edit(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('book_list')
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, '图书更新成功')
        return redirect('book_list')
    return render(request, 'books/book_form.html', {'form': form, 'title': '编辑图书'})


@login_required
def book_delete(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('book_list')
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, '图书删除成功')
        return redirect('book_list')
    return render(request, 'confirm_delete.html', {'obj': book, 'cancel_url': reverse('book_list')})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    copies = book.bookcopy_set.all()
    return render(request, 'books/book_detail.html', {'book': book, 'copies': copies})


# --- Category ---
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'books/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('category_list')
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, '分类添加成功')
        return redirect('category_list')
    return render(request, 'books/category_form.html', {'form': form, 'title': '新增分类'})


@login_required
def category_edit(request, pk):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('category_list')
    cat = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=cat)
    if form.is_valid():
        form.save()
        messages.success(request, '分类更新成功')
        return redirect('category_list')
    return render(request, 'books/category_form.html', {'form': form, 'title': '编辑分类'})


@login_required
def category_delete(request, pk):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('category_list')
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, '分类删除成功')
        return redirect('category_list')
    return render(request, 'confirm_delete.html', {'obj': cat, 'cancel_url': reverse('category_list')})

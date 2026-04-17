from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import BorrowRecord
from .forms import BorrowForm
from apps.catalog.models import BookCopy


@login_required
def borrow_list(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    qs = BorrowRecord.objects.select_related('reader', 'book_copy__book').order_by('-borrow_date')
    status = request.GET.get('status', '')
    q = request.GET.get('q', '')
    if status:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(reader__name__icontains=q) | qs.filter(book_copy__book__title__icontains=q)
    # 自动标记逾期
    today = timezone.localdate()
    qs.filter(status='borrowed', due_date__lt=today).update(status='overdue')
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'borrow/borrow_list.html', {
        'page_obj': page, 'status': status, 'q': q,
        'status_choices': BorrowRecord.STATUS_CHOICES
    })


@login_required
def borrow_create(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('borrow_list')
    form = BorrowForm(request.POST or None)
    if form.is_valid():
        reader = form.cleaned_data['reader']
        book_copy = form.cleaned_data['book_copy']
        if reader.status == 'suspended':
            messages.error(request, '该读者账号已挂起，无法借阅')
        elif reader.current_borrow_count() >= reader.max_borrow:
            messages.error(request, f'该读者已达最大借阅数量({reader.max_borrow}本)')
        elif book_copy.status != 'available':
            messages.error(request, '该副本当前不可借')
        else:
            borrow_days = getattr(settings, 'BORROW_DAYS', 30)
            record = form.save(commit=False)
            record.borrow_date = timezone.localdate()
            record.due_date = timezone.localdate() + timedelta(days=borrow_days)
            record.status = 'borrowed'
            record.save()
            book_copy.status = 'borrowed'
            book_copy.save()
            book = book_copy.book
            book.available_copies = book.bookcopy_set.filter(status='available').count()
            book.save()
            messages.success(request, '借阅登记成功')
            return redirect('borrow_list')
    return render(request, 'borrow/borrow_form.html', {'form': form, 'title': '借书登记'})


@login_required
def borrow_return(request, pk):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('borrow_list')
    record = get_object_or_404(BorrowRecord, pk=pk)
    if record.status == 'returned':
        messages.warning(request, '该记录已归还')
        return redirect('borrow_list')
    if request.method == 'POST':
        record.return_date = timezone.localdate()
        record.fine = record.calc_fine()
        record.status = 'returned'
        record.save()
        copy = record.book_copy
        copy.status = 'available'
        copy.save()
        book = copy.book
        book.available_copies = book.bookcopy_set.filter(status='available').count()
        book.save()
        messages.success(request, f'还书成功，罚金：{record.fine} 元')
        return redirect('borrow_list')
    return render(request, 'borrow/borrow_return.html', {'record': record})


from .models import BorrowRequest
from apps.books.models import Book


@login_required
def my_borrows(request):
    """读者查看自己的借阅记录"""
    try:
        reader = request.user.reader
    except Exception:
        messages.error(request, '您还没有关联读者档案，请联系管理员')
        return redirect('dashboard')
    records = BorrowRecord.objects.filter(reader=reader).select_related('book_copy__book').order_by('-borrow_date')
    requests_qs = BorrowRequest.objects.filter(reader=reader).select_related('book').order_by('-created_at')
    return render(request, 'borrow/my_borrows.html', {'records': records, 'requests': requests_qs, 'reader': reader})


@login_required
def borrow_request_create(request):
    """读者自助申请借书"""
    try:
        reader = request.user.reader
    except Exception:
        messages.error(request, '您还没有关联读者档案，请联系管理员')
        return redirect('dashboard')
    books = Book.objects.filter(status='available', available_copies__gt=0).select_related('category')
    # 当前借阅中 + 待审批申请数，合计不能超过上限
    pending_count = BorrowRequest.objects.filter(reader=reader, status='pending').count()
    current_total = reader.current_borrow_count() + pending_count
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)
        # 重新计算，防止并发
        pending_count = BorrowRequest.objects.filter(reader=reader, status='pending').count()
        current_total = reader.current_borrow_count() + pending_count
        if reader.status == 'suspended':
            messages.error(request, '您的账号已挂起，无法申请借书')
        elif current_total >= reader.max_borrow:
            messages.error(request, f'您当前借阅+待审批申请已达上限（{reader.max_borrow}本），请还书或等待审批完成后再申请')
        elif BorrowRequest.objects.filter(reader=reader, book=book, status='pending').exists():
            messages.warning(request, '您已申请过该书，请等待审批')
        else:
            BorrowRequest.objects.create(reader=reader, book=book)
            messages.success(request, '借书申请已提交，请等待馆员审批')
            return redirect('my_borrows')
    return render(request, 'borrow/borrow_request_form.html', {
        'books': books,
        'reader': reader,
        'current_total': current_total,
    })


@login_required
def borrow_request_cancel(request, pk):
    """读者取消申请"""
    try:
        reader = request.user.reader
    except Exception:
        return redirect('dashboard')
    req = get_object_or_404(BorrowRequest, pk=pk, reader=reader)
    if req.status == 'pending':
        req.status = 'cancelled'
        req.save()
        messages.success(request, '申请已取消')
    return redirect('my_borrows')


@login_required
def borrow_request_list(request):
    """馆员查看所有借书申请"""
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    qs = BorrowRequest.objects.filter(status='pending').select_related('reader', 'book').order_by('created_at')
    # 为每条申请附加读者当前借阅数和待审批数，方便馆员判断
    for req in qs:
        req.reader_borrow_count = req.reader.current_borrow_count()
        req.reader_pending_count = BorrowRequest.objects.filter(reader=req.reader, status='pending').count()
    return render(request, 'borrow/borrow_request_list.html', {'requests': qs})


@login_required
def borrow_request_approve(request, pk):
    """馆员审批借书申请"""
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('dashboard')
    req = get_object_or_404(BorrowRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            copy = req.book.bookcopy_set.filter(status='available').first()
            if not copy:
                messages.error(request, '该书暂无可借副本')
            elif req.reader.current_borrow_count() >= req.reader.max_borrow:
                messages.error(request, f'该读者已达最大借阅数量（{req.reader.max_borrow}本），无法批准')
            else:
                from django.conf import settings
                from datetime import timedelta
                record = BorrowRecord.objects.create(
                    reader=req.reader,
                    book_copy=copy,
                    borrow_date=timezone.localdate(),
                    due_date=timezone.localdate() + timedelta(days=getattr(settings, 'BORROW_DAYS', 30)),
                    status='borrowed',
                )
                copy.status = 'borrowed'
                copy.save()
                book = copy.book
                book.available_copies = book.bookcopy_set.filter(status='available').count()
                book.save()
                req.status = 'approved'
                req.borrow_record = record
                req.save()
                messages.success(request, f'已批准 {req.reader.name} 借阅《{req.book.title}》')
        elif action == 'reject':
            req.status = 'rejected'
            req.reject_reason = request.POST.get('reject_reason', '')
            req.save()
            messages.success(request, '已拒绝申请')
        return redirect('borrow_request_list')
    return render(request, 'borrow/borrow_request_approve.html', {'req': req})

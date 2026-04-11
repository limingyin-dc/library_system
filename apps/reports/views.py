from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from apps.books.models import Book, Category
from apps.borrow.models import BorrowRecord
from apps.purchase.models import PurchaseOrder
from apps.readers.models import Reader


@login_required
def report_index(request):
    if not request.user.is_librarian():
        messages.error(request, '权限不足')
        return redirect('dashboard')

    # 各分类图书数量
    category_data = list(
        Category.objects.annotate(book_count=Count('book')).values('name', 'book_count')
    )

    # 近12个月借阅趋势
    from django.db.models.functions import TruncMonth
    from django.utils import timezone
    import datetime
    twelve_months_ago = timezone.localdate() - datetime.timedelta(days=365)
    borrow_trend = list(
        BorrowRecord.objects.filter(borrow_date__gte=twelve_months_ago)
        .annotate(month=TruncMonth('borrow_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # 采购状态统计
    purchase_stats = list(
        PurchaseOrder.objects.values('status').annotate(count=Count('id'))
    )

    context = {
        'total_books': Book.objects.count(),
        'total_readers': Reader.objects.count(),
        'total_borrows': BorrowRecord.objects.count(),
        'active_borrows': BorrowRecord.objects.filter(status='borrowed').count(),
        'overdue_borrows': BorrowRecord.objects.filter(status='overdue').count(),
        'category_labels': [d['name'] for d in category_data],
        'category_counts': [d['book_count'] for d in category_data],
        'borrow_months': [str(d['month'])[:7] for d in borrow_trend],
        'borrow_counts': [d['count'] for d in borrow_trend],
        'purchase_stats': purchase_stats,
    }
    return render(request, 'reports/report_index.html', context)

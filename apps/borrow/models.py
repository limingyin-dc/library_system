from django.db import models
from django.utils import timezone
from apps.catalog.models import BookCopy
from apps.readers.models import Reader
from apps.books.models import Book


class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('borrowed', '借阅中'),
        ('returned', '已归还'),
        ('overdue', '已逾期'),
    ]
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, verbose_name='图书副本')
    borrow_date = models.DateField('借阅日期', default=timezone.localdate)
    due_date = models.DateField('应还日期')
    return_date = models.DateField('实际归还日期', null=True, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='borrowed')
    fine = models.DecimalField('罚金', max_digits=8, decimal_places=2, default=0)
    notes = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '借阅记录'
        verbose_name_plural = '借阅记录'

    def __str__(self):
        return f'{self.reader.name} - {self.book_copy.book.title}'

    def is_overdue(self):
        if self.status == 'borrowed':
            return timezone.localdate() > self.due_date
        return False

    def calc_fine(self):
        from django.conf import settings
        if self.is_overdue():
            days = (timezone.localdate() - self.due_date).days
            return round(days * getattr(settings, 'FINE_PER_DAY', 0.5), 2)
        return 0


class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('cancelled', '已取消'),
    ]
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='申请图书')
    request_date = models.DateField('申请日期', default=timezone.localdate)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    reject_reason = models.CharField('拒绝原因', max_length=200, blank=True)
    borrow_record = models.OneToOneField(BorrowRecord, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='借阅记录')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '借书申请'
        verbose_name_plural = '借书申请'

    def __str__(self):
        return f'{self.reader.name} 申请 {self.book.title}'

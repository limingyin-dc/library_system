from django.db import models
from apps.books.models import Book


class BookCopy(models.Model):
    STATUS_CHOICES = [
        ('available', '可借'),
        ('borrowed', '已借出'),
        ('damaged', '损坏'),
        ('lost', '丢失'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='图书')
    barcode = models.CharField('条形码', max_length=50, unique=True)
    location = models.CharField('馆藏位置', max_length=100, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='available')
    cataloged_at = models.DateTimeField('编目时间', auto_now_add=True)
    notes = models.TextField('备注', blank=True)

    class Meta:
        verbose_name = '图书副本'
        verbose_name_plural = '图书副本'

    def __str__(self):
        return f'{self.book.title} - {self.barcode}'

from django.db import models
from apps.books.models import Book


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('ordered', '已订购'),
        ('received', '已入库'),
        ('rejected', '不合格/退货'),
        ('cancelled', '已取消'),
    ]
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联图书（到货后填写）')
    book_title = models.CharField('书名', max_length=200)
    quantity = models.IntegerField('采购数量', default=1)
    supplier = models.CharField('供应商', max_length=100, blank=True)
    order_date = models.DateField('采购日期')
    expected_date = models.DateField('预计到货日期', null=True, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField('单价', max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '采购记录'
        verbose_name_plural = '采购记录'

    def __str__(self):
        return f'{self.book_title} x{self.quantity}'

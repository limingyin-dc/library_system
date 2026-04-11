from django.db import models
from django.conf import settings


class Reader(models.Model):
    STATUS_CHOICES = [
        ('active', '正常'),
        ('suspended', '挂起'),
    ]
    name = models.CharField('姓名', max_length=50)
    card_no = models.CharField('借书证号', max_length=30, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联账号')
    id_card = models.CharField('身份证号', max_length=18, blank=True)
    phone = models.CharField('电话', max_length=20, blank=True)
    email = models.EmailField('邮箱', blank=True)
    address = models.CharField('地址', max_length=200, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='active')
    max_borrow = models.IntegerField('最大借阅数', default=5)
    created_at = models.DateTimeField('注册时间', auto_now_add=True)

    class Meta:
        verbose_name = '读者'
        verbose_name_plural = '读者'

    def __str__(self):
        return f'{self.name}({self.card_no})'

    def current_borrow_count(self):
        return self.borrowrecord_set.filter(status='borrowed').count()

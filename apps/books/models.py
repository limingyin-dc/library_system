from django.db import models


class Category(models.Model):
    name = models.CharField('分类名称', max_length=100, unique=True)
    description = models.TextField('描述', blank=True)

    class Meta:
        verbose_name = '图书分类'
        verbose_name_plural = '图书分类'

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = [
        ('available', '可借'),
        ('unavailable', '不可借'),
    ]
    title = models.CharField('书名', max_length=200)
    author = models.CharField('作者', max_length=100)
    publisher = models.CharField('出版社', max_length=100)
    isbn = models.CharField('ISBN', max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    total_copies = models.IntegerField('总副本数', default=0)
    available_copies = models.IntegerField('可借副本数', default=0)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='available')
    publish_date = models.DateField('出版日期', null=True, blank=True)
    description = models.TextField('简介', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'

    def __str__(self):
        return self.title

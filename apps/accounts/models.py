from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('librarian', '馆员'),
        ('reader', '读者'),
    ]
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='reader')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def is_admin(self):
        return self.role == 'admin'

    def is_librarian(self):
        return self.role in ('admin', 'librarian')

    def __str__(self):
        return f'{self.username}({self.get_role_display()})'

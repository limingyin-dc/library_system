"""
初始化数据脚本，运行方式：
    python manage.py shell < init_data.py
或者直接：
    python init_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from apps.accounts.models import User
from apps.books.models import Category, Book
from apps.readers.models import Reader

# 创建管理员
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
    print('创建管理员: admin / admin123')

# 创建馆员
if not User.objects.filter(username='librarian').exists():
    u = User.objects.create_user('librarian', password='lib123', role='librarian')
    print('创建馆员: librarian / lib123')

# 创建读者用户
if not User.objects.filter(username='reader1').exists():
    u = User.objects.create_user('reader1', password='reader123', role='reader')
    print('创建读者: reader1 / reader123')

# 创建分类
categories = ['文学', '历史', '科技', '经济', '哲学', '艺术']
for name in categories:
    Category.objects.get_or_create(name=name)
print(f'创建分类: {categories}')

# 创建示例图书
books_data = [
    ('红楼梦', '曹雪芹', '人民文学出版社', '9787020002207', '文学'),
    ('三国演义', '罗贯中', '人民文学出版社', '9787020008728', '文学'),
    ('史记', '司马迁', '中华书局', '9787101003048', '历史'),
    ('Python编程', 'Eric Matthes', '人民邮电出版社', '9787115428028', '科技'),
    ('经济学原理', '曼昆', '北京大学出版社', '9787301105528', '经济'),
]
for title, author, publisher, isbn, cat_name in books_data:
    cat = Category.objects.get(name=cat_name)
    Book.objects.get_or_create(isbn=isbn, defaults={
        'title': title, 'author': author, 'publisher': publisher,
        'category': cat, 'total_copies': 3, 'available_copies': 3
    })
print('创建示例图书完成')

# 创建示例读者
readers_data = [
    ('张三', 'R001', '13800000001'),
    ('李四', 'R002', '13800000002'),
    ('王五', 'R003', '13800000003'),
]
for name, card_no, phone in readers_data:
    Reader.objects.get_or_create(card_no=card_no, defaults={'name': name, 'phone': phone})
print('创建示例读者完成')

print('\n初始化完成！访问 http://127.0.0.1:8000 登录系统')

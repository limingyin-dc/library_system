"""
运行方式: python manage.py shell < insert_test_data.py
"""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from datetime import date
from apps.books.models import Category, Book
from apps.catalog.models import BookCopy

# 分类
categories = [
    ('计算机', '计算机科学与技术类书籍'),
    ('文学', '中外文学名著'),
    ('历史', '历史与人文类书籍'),
    ('经济', '经济与管理类书籍'),
    ('科学', '自然科学类书籍'),
]
cat_objs = {}
for name, desc in categories:
    c, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
    cat_objs[name] = c

# 图书数据
books_data = [
    ('Python编程：从入门到实践', 'Eric Matthes', '人民邮电出版社', '9787115428028', '计算机', '2016-07-01', 3),
    ('深入理解计算机系统', 'Randal E. Bryant', '机械工业出版社', '9787111544937', '计算机', '2016-11-01', 2),
    ('算法导论', 'Thomas H. Cormen', '机械工业出版社', '9787111187776', '计算机', '2013-01-01', 2),
    ('Django实战', '刘天斯', '机械工业出版社', '9787111603800', '计算机', '2018-06-01', 2),
    ('红楼梦', '曹雪芹', '人民文学出版社', '9787020002207', '文学', '1996-12-01', 3),
    ('三国演义', '罗贯中', '人民文学出版社', '9787020008728', '文学', '1998-05-01', 2),
    ('活着', '余华', '作家出版社', '9787506365437', '文学', '2012-08-01', 3),
    ('百年孤独', '加西亚·马尔克斯', '南海出版公司', '9787544253994', '文学', '2011-06-01', 2),
    ('人类简史', '尤瓦尔·赫拉利', '中信出版社', '9787508660752', '历史', '2014-11-01', 3),
    ('明朝那些事儿', '当年明月', '中国海关出版社', '9787801657152', '历史', '2009-04-01', 2),
    ('经济学原理', 'N·格里高利·曼昆', '北京大学出版社', '9787301105528', '经济', '2012-01-01', 2),
    ('国富论', '亚当·斯密', '商务印书馆', '9787100010054', '经济', '1972-01-01', 2),
    ('时间简史', '史蒂芬·霍金', '湖南科学技术出版社', '9787535732309', '科学', '2012-01-01', 3),
    ('自私的基因', '理查德·道金斯', '中信出版社', '9787508648309', '科学', '2012-09-01', 2),
]

barcode_counter = 1000
for title, author, publisher, isbn, cat_name, pub_date, copies in books_data:
    book, created = Book.objects.get_or_create(
        isbn=isbn,
        defaults={
            'title': title,
            'author': author,
            'publisher': publisher,
            'category': cat_objs[cat_name],
            'publish_date': date.fromisoformat(pub_date),
            'total_copies': copies,
            'available_copies': copies,
            'status': 'available',
        }
    )
    if created:
        for i in range(copies):
            barcode_counter += 1
            BookCopy.objects.create(
                book=book,
                barcode=f'BC{barcode_counter:06d}',
                location=f'{cat_name}区-{barcode_counter % 10 + 1}架',
                status='available',
            )
        print(f'已添加: {title} ({copies}本)')
    else:
        print(f'已存在: {title}')

print('\n测试数据插入完成！')

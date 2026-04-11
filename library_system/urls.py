from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('books/', include('apps.books.urls')),
    path('purchase/', include('apps.purchase.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('borrow/', include('apps.borrow.urls')),
    path('readers/', include('apps.readers.urls')),
    path('reports/', include('apps.reports.urls')),
]

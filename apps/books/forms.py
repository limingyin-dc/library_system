from django import forms
from .models import Book, Category
from apps.mixins import BootstrapMixin


class BookForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'isbn', 'category',
                  'total_copies', 'available_copies', 'status', 'publish_date', 'description']
        widgets = {
            'publish_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CategoryForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

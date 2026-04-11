from django import forms
from .models import BorrowRecord
from apps.catalog.models import BookCopy
from apps.mixins import BootstrapMixin


class BorrowForm(BootstrapMixin, forms.ModelForm):
    book_copy = forms.ModelChoiceField(
        queryset=BookCopy.objects.filter(status='available').select_related('book'),
        label='图书副本'
    )

    class Meta:
        model = BorrowRecord
        fields = ['reader', 'book_copy', 'notes']

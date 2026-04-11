from django import forms
from .models import BookCopy
from apps.mixins import BootstrapMixin


class BookCopyForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['book', 'barcode', 'location', 'status', 'notes']

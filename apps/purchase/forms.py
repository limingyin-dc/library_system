from django import forms
from .models import PurchaseOrder
from apps.mixins import BootstrapMixin


class PurchaseOrderForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['book', 'book_title', 'quantity', 'supplier', 'order_date',
                  'expected_date', 'status', 'price', 'notes']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_date': forms.DateInput(attrs={'type': 'date'}),
        }

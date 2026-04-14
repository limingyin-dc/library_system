from django import forms
from .models import PurchaseOrder
from apps.mixins import BootstrapMixin


class PurchaseOrderForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['book_title', 'book', 'quantity', 'supplier', 'order_date',
                  'expected_date', 'status', 'price', 'notes']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].required = False
        self.fields['book'].help_text = '图书到货入库后再关联，采购时可留空'
        self.fields['book_title'].help_text = '采购时填写书名，无需图书已存在'

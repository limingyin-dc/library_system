from django import forms
from .models import Reader
from apps.mixins import BootstrapMixin


class ReaderForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['name', 'card_no', 'id_card', 'phone', 'email', 'address', 'status', 'max_borrow', 'user']

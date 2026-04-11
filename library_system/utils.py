"""给所有表单字段自动添加 Bootstrap form-control class"""
from django import forms


def add_bootstrap_classes(form):
    for field_name, field in form.fields.items():
        widget = field.widget
        if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput,
                               forms.NumberInput, forms.DateInput, forms.Textarea,
                               forms.URLInput)):
            widget.attrs.setdefault('class', 'form-control')
        elif isinstance(widget, forms.Select):
            widget.attrs.setdefault('class', 'form-select')
        elif isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault('class', 'form-check-input')
    return form

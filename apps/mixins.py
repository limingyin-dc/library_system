from django import forms


class BootstrapMixin:
    """自动给表单字段添加 Bootstrap 样式"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            w = field.widget
            if isinstance(w, (forms.TextInput, forms.EmailInput, forms.PasswordInput,
                               forms.NumberInput, forms.DateInput, forms.Textarea, forms.URLInput)):
                w.attrs.setdefault('class', 'form-control')
            elif isinstance(w, forms.Select):
                w.attrs.setdefault('class', 'form-select')
            elif isinstance(w, forms.CheckboxInput):
                w.attrs.setdefault('class', 'form-check-input')

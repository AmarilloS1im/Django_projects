from django import forms
from products.models import Size

class CheckboxForm(forms.Form):
    checkbox_size = forms.CharField(widget=forms.CheckboxInput(attrs={
    'class':'size_checkbox', 'type':'checkbox', 'name':'size_checkbox','id':"size_checkbox_form"}),required=True)

    class Meta:
        model = Size
        fields = ('checkbox_size')
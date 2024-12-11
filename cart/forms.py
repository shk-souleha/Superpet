from .models import order
from django import forms

class OrderForm(forms.ModelForm):
    class Meta:
        model=order
        fields="__all__"
        exclude=['order_id','user','paid']
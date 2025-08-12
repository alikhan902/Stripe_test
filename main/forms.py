from django import forms
from django.core.exceptions import ValidationError
from .models import Order

# Запрет на использование разных валют в одной модели Order
class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        items = cleaned_data.get('items')
        if items:
            currencies = set(item.currency for item in items)
            if len(currencies) > 1:
                raise ValidationError("Все товары в заказе должны быть в одной валюте.")
            cleaned_data['currency'] = currencies.pop()
        return cleaned_data

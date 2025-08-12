from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ValidationError

class Item(models.Model):
    name = models.CharField(max_length=200)  # Название товара
    description = models.TextField(blank=True)  # Описание товара (может быть пустым)
    price = models.PositiveIntegerField(help_text='Price in cents')  # Цена в центах (только положительные значения)
    currency = models.CharField(
        max_length=3, 
        default='usd', 
        choices=[('usd', 'USD'), ('rub', 'RUB')]  # Валюта товара: USD или RUB
    )

    def __str__(self):
        return self.name  # Возвращает название товара для удобства отображения


class Order(models.Model):
    items = models.ManyToManyField(Item)  # Связь с товарами (много ко многим)
    
    def total_amount(self):
        """
        Подсчитывает итоговую сумму заказа с учётом скидки и налога.
        Если скидка или налог не заданы, берёт значение по умолчанию.
        """
        disc = 1.0  # Начальное значение скидки (без скидки)
        tax = 1.0   # Начальное значение налога (без налога)
        if hasattr(self, 'discount'):
            disc = disc - (self.discount.discount_percentage) / 100  # Вычитаем скидку (в процентах)
        if hasattr(self, 'tax'):
            tax = tax + (self.tax.tax_percentage) / 100  # Добавляем налог (в процентах)
        
        # Суммируем цены всех товаров, применяем скидку и налог, возвращаем целое число (цены в центах)
        return int(sum(item.price for item in self.items.all()) * disc * tax)

    
class Discount(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # Связь с заказом (один к одному)
    discount_percentage = models.FloatField(
        default=1.0, 
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]  # Валидаторы: от 0 до 100 процентов
    )
    
class Tax(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # Связь с заказом (один к одному)
    tax_percentage = models.FloatField(
        default=1.0, 
        validators=[MinValueValidator(0.0)]  # Валидатор: не может быть меньше 0
    )

import stripe
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY  # Инициализация Stripe с секретным ключом


def item_page(request, pk):
    """
    Отображает страницу отдельного товара.
    """
    item = get_object_or_404(Item, pk=pk)  # Получаем объект Item или 404
    context = {
        'item': item,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,  # Публикуемый ключ Stripe
    }
    return render(request, 'main/item.html', context)  # Рендерим шаблон с контекстом


def order_page(request, pk):
    """
    Отображает страницу заказа.
    """
    order = get_object_or_404(Order, pk=pk)  # Получаем объект Order или 404
    context = {
        'total_amount': order.total_amount(),  # Итоговая сумма с учетом скидок и налогов
        'order': order,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,  # Публикуемый ключ Stripe
    }
    return render(request, 'main/order.html', context)  # Рендерим шаблон с контекстом


def buy_item(request, pk):
    """
    Создает платежный интент Stripe для оплаты одного товара.
    """
    item = get_object_or_404(Item, pk=pk)  # Получаем объект Item или 404

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(item.price),  # Цена товара в центах
            currency=item.currency,  # Валюта товара
            description=f"{item.name} - {item.description}",  # Описание платежа
            automatic_payment_methods={'enabled': True,}
            )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Возвращаем ошибку в JSON

    return JsonResponse({'client_secret': intent.client_secret})  # Возвращаем client_secret


def buy_order(request, pk):
    """
    Создает платежный интент Stripe для оплаты заказа.
    """
    order = get_object_or_404(Order, pk=pk)   
    total_amount = order.total_amount()  # Итоговая сумма заказа
    currencies = set(item.currency for item in order.items.all())  # Все валюты товаров в заказе
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency=currencies.pop(),  # Берет одну валюту из множества
            description=f"Order #{order.id} - {order.items.count()} items",  # Описание платежа
            automatic_payment_methods={'enabled': True}
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Возвращаем ошибку в JSON

    return JsonResponse({'client_secret': intent.client_secret})  # Возвращаем client_secret

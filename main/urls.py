from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:pk>/', views.item_page, name='item_page'),
    path('order/<int:pk>/', views.order_page, name='order_page'),
    path('buy/<int:pk>/', views.buy_item, name='buy_item'),
    path('buy-order/<int:pk>/', views.buy_order, name='buy_order'),
]
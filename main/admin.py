from django.contrib import admin
from .models import Item, Order, Discount, Tax
from .models import Order
from .forms import OrderAdminForm


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm

admin.site.register(Item)
admin.site.register(Discount)
admin.site.register(Tax)
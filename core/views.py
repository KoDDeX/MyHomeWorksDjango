from django.shortcuts import render
from django.http import HttpResponse
from .data import *

# Create your views here.
def landing(request):
    context = {
        'menu_items': MENU_ITEMS,
    }
    return render(request, 'landing.html', context)

def thanks(request):
    context = {
        'menu_items': MENU_ITEMS,
    }
    return render(request, 'core/thanks.html', context)

def orders_list(request):
    context = {
        'orders': orders,
        'menu_items': MENU_ITEMS,
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id):
    try:
        order = [o for o in orders if o["id"] == order_id][0]
    except IndexError:
        # Если заказ не найден, возвращаем 404 - данные не найдены
        return HttpResponse(status=404)

    context = {
        "order": order,
        'menu_items': MENU_ITEMS,
    }
    return render(request, 'core/order_detail.html', context)
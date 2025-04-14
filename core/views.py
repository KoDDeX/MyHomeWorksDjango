from django.shortcuts import render
from django.http import HttpResponse
from .data import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def landing(request):
    context = {
        'services': services,
        'masters': masters,
    }
    return render(request, 'core/landing.html', context)

def thanks(request):
    context = {
        'menu_items': MENU_ITEMS,
    }
    return render(request, 'core/thanks.html', context)

@login_required
def orders_list(request):
    context = {
        'orders': orders,
        'menu_items': MENU_ITEMS,
    }
    return render(request, 'core/orders_list.html', context)

@login_required
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
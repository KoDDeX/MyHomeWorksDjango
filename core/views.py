from django.shortcuts import render
from django.http import HttpResponse
from .data import *

# Create your views here.
def landing(request):
    return render(request, 'landing.html')

def thanks(request):
    return render(request, 'core/thanks.html')

def orders_list(request):
    context = {
        'orders': orders
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id):
    try:
        order = [o for o in orders if o["id"] == order_id][0]
    except IndexError:
        # Если заказ не найден, возвращаем 404 - данные не найдены
        return HttpResponse(status=404)

    context = {
        "order": order
    }
    return render(request, 'core/order_detail.html', context)
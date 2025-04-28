from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .data import *
from django.contrib.auth.decorators import login_required
from .models import Review, Order, Master, Service
from django.db.models import Q

# Create your views here.
def landing(request):
    context = {
        'services': Service.objects.all(),
        'masters': Master.objects.all(),
        'reviews': Review.objects.all(),
    }
    return render(request, 'core/landing.html', context)

def thanks(request):
    return render(request, 'core/thanks.html')

@login_required
def orders_list(request):
    """
    Функция для отображения списка заказов. Для привилегированных пользователей
    """
    if request.method == "GET":
        all_orders = Order.objects.select_related("master").prefetch_related("services").all()
        search_query = request.GET.get('search', None)
        if search_query:
            check_boxes = request.GET.getlist('search_in')
            filters = Q()
            if "name" in check_boxes:
                filters |= Q(client_name__icontains=search_query)
            if "phone" in check_boxes:
                filters = filters | Q(phone__icontains=search_query)
            if "comment" in check_boxes:
                filters |= Q(comment__icontains=search_query)
            if filters:
                all_orders = all_orders.filter(filters)


    context = {
        'orders': all_orders,
    }
    return render(request, 'core/orders_list.html', context)

@login_required
def order_detail(request, order_id):
    """
    Функция для отображения информации о заказе по его идентификатору.
    """
    order = get_object_or_404(Order, id=order_id)

    context = {
        "order": order,
        "title": f"Заказ №{order_id}",  
    }
    return render(request, 'core/order_detail.html', context)

@login_required
def service_create(request):
    """
    Функция для создания нового заказа.
    """
    if request.method == "GET":
        context = {
            "title": "Создание услуги",
        }
        return render(request, 'core/service_create.html', context)
    elif request.method == "POST":
        pass
        # client_name = request.POST.get("client_name")
        # phone = request.POST.get("phone")
        # comment = request.POST.get("comment")
        # appointment_date = request.POST.get("appointment_date")
        # master_id = request.POST.get("master")
        # service_ids = request.POST.getlist("service")
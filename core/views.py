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


# order = Order.objects.create(
#     client_name="Иван Иванов",
#     phone="+79991234567",
#     comment="Нужно сделать стрижку",
#     status="not_approved",
#     appointment_date='2025-10-01 10:00:00',
#     master=Master.objects.get(id=1),
#     services=Service.objects.get(id=1),
# )

# Service.objects.create(
#     name="Стрижка",
#     price=1000,
#     duration=60,
#     description="Стрижка мужского волоса",
# )
# Service.objects.create(
#     name="Стрижка + борода",
#     price=1500,
#     duration=90,
#     description="Стрижка мужского волоса и бороды",
# )

# Service.objects.create(
#     name="Покраска бороды",
#     price=2000,
#     duration=120,
#     description="Покраска бороды и усов из мужского волоса",
# )

# Service.objects.create(
#     name="Покраска волос",
#     price=2500,
#     duration=150,
#     description="Покраска волос мужского волоса",
# )

# Service.objects.create(
#     name="Покраска волос + борода",
#     price=3000,
#     duration=180,
#     description="Покраска волос и бороды из мужского волоса",
# )

# Service.objects.create(
#     name="Стрижка Сахара",
#     price=3500,
#     duration=210,
#     description="Стрижка наголо",
# )
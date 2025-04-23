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

# Master.objects.create(
#     name="Степан 'Секира' Ильич",
#     photo="masters/ivan.jpg",
#     phone="+79995556677",
#     address="ул. Пушкина, д. 1",
#     experience=5,
#     is_active=True,
# )

# Master.objects.create(
#     name="Юрий 'Фен' Петров",
#     photo="masters/ivan.jpg",
#     phone="+79995556677",
#     address="ул. Ленина, д. 2",
#     experience=3,
#     is_active=True,
# )

# Master.objects.create(
#     name="Ираклий 'Зодиак' Иванов",
#     photo="masters/ivan.jpg",
#     phone="+79995556677",
#     address="ул. Гагарина, д. 3",
#     experience=10,
#     is_active=True,
# )

# master = Master.objects.get(id=1)
# service = Service.objects.get(id=1)
# order = Order.objects.create(
#     client_name="Иван Иванов",
#     phone="+79991234567",
#     comment="Нужно сделать стрижку",
#     status="not_approved",
#     appointment_date='2025-10-01 10:00:00',
#     master=master,
# )
# order.services.add(service)

# master = Master.objects.get(id=2)
# service = Service.objects.get(id=2)
# order = Order.objects.create(
#     client_name="Вася Пупкин",
#     phone="+79997654321",
#     comment="Очень надо",
#     status="not_approved",
#     appointment_date='2025-10-11 10:00:00',
#     master=master,
# )
# order.services.add(service)

# master = Master.objects.get(id=3)
# service = Service.objects.filter(id__in=[3, 4])
# order = Order.objects.create(
#     client_name="Петя Васечкин",
#     phone="+79997777777",
#     comment="Подстричся бы",
#     status="not_approved",
#     appointment_date='2025-10-21 10:00:00',
#     master=master,
# )
# order.services.add(*service)

# master = Master.objects.get(id=1)
# review = Review.objects.create(
#     client_name="Иван Иванов",
#     text="Отличная работа, рекомендую!",
#     rating=5,
#     master=master,
# )
# review.save()

# master = Master.objects.get(id=2)
# review = Review.objects.create(
#     client_name="Фрося Фролова",
#     text="Есть над чем поработать!",
#     rating=4,
#     master=master,
# )
# review.save()

# master = Master.objects.get(id=3)
# review = Review.objects.create(
#     client_name="Тимофей Сергеевич",
#     text="Больше не приду, уже не хочу!",
#     rating=1,
#     master=master,
# )
# review.save()
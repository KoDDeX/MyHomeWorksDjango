from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .data import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review, Order, Master, Service
from django.db.models import Q
from .forms import ReviewForm, OrderForm
import json

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
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        duration = request.POST.get("duration")
        is_popular = request.POST.get("is_popular")

        if name and price and description:
            new_service = Service.objects.create(
                name=name,
                price=price,
                description=description,
            )
            if is_popular:
                new_service.is_popular = True
                new_service.save()
            if duration:
                new_service.duration = duration
                new_service.save()
            return redirect("landing")
        
        else:
            # Если данные не введены, возвращаем ошибку
            return HttpResponse("Ошибка: все поля должны быть заполнены!")

def review_create(request):

    if request.method == "GET":
        form = ReviewForm()
        context = {
            "title": "Создание отзыва",
            "form": form,
        }
        return render(request, "core/review_form.html", context)

    elif request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("thanks")
        else:
            context = {
                "title": "Создание отзыва",
                "form": form,
            }
            return render(request, "core/review_form.html", context)

def get_master_info(request):
    """
    Универсальное представление для получения информации о мастере через AJAX.
    Возвращает данные мастера в формате JSON.
    """
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        master_id = request.GET.get('master_id')
        if master_id:
            try:
                master = Master.objects.get(pk=master_id)
                # Формируем данные для ответа
                master_data = {
                    'id': master.id,
                    'name': f"{master.name}",
                    'experience': master.experience,
                    'photo': master.photo.url if master.photo else None,
                    'services': list(master.services.values('id', 'name', 'price')),
                }
                return JsonResponse({'success': True, 'master': master_data})
            except Master.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Мастер не найден'})
        return JsonResponse({'success': False, 'error': 'Не указан ID мастера'})
    return JsonResponse({'success': False, 'error': 'Недопустимый запрос'})

def masters_services_by_id(request, master_id=None):
    """
    Вью для ajax запросов фронтенда, для подгрузки услуг конкретного мастера в форму
    m2m выбора услуг
    """
    # Если master_id не передан в URL, пробуем получить его из POST-запроса
    if master_id is None:
        data = json.loads(request.body)
        master_id = data.get("master_id")

    # Получаем мастера по id
    master = get_object_or_404(Master, id=master_id)

    # Получаем услуги
    services = master.services.all()

    # Формируем ответ в виде JSON
    response_data = []

    for service in services:
        # Добавляем в ответ id и название услуги
        response_data.append(
            {
                "id": service.id,
                "name": service.name,
            }
        )
    # Возвращаем ответ в формате JSON
    return HttpResponse(
        json.dumps(response_data, ensure_ascii=False, indent=4),
        content_type="application/json",
    )

def order_create(request):
    """
    Вью для создания заказа
    """
    if request.method == "GET":
        # Если метод GET - возвращаем пустую форму
        form = OrderForm()

        context = {
            "title": "Создание заказа",
            "form": form,
            "button_text": "Создать",
        }
        return render(request, "core/order_form.html", context)

    if request.method == "POST":
        # Создаем форму и передаем в нее POST данные
        form = OrderForm(request.POST)

        # Если форма валидна:
        if form.is_valid():
            # Сохраняем форму в БД
            form.save()
            client_name = form.cleaned_data.get("client_name")
            # Даем пользователю уведомление об успешном создании
            messages.success(request, f"Заказ для {client_name} успешно создан!")

            # Перенаправляем на страницу с благодарностью
            return redirect("thanks")

        # В случае ошибок валидации Django автоматически заполнит form.errors
        # и отобразит их в шаблоне, поэтому просто возвращаем форму
        context = {
            "title": "Создание заказа",
            "form": form,
            "button_text": "Создать",
        }
        return render(request, "core/order_form.html", context)
from django.contrib import admin
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('thanks/<str:source>/', ThanksView.as_view(), name='thanks'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('services/create/', service_create, name='service_create'),
    path("masters_services/", masters_services_by_id, name="masters_services_by_id_ajax"),
    path("order_create/", order_create, name="order_create"),
    path('review/create/', review_create, name='review_create'),
]
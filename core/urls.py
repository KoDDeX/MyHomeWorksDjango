from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('services/create/', views.service_create, name='service_create'),
    path("masters_services/", views.masters_services_by_id, name="masters_services_by_id_ajax"),
    path("order_create/", views.order_create, name="order_create"),
    path('review/create/', views.review_create, name='review_create'),
]
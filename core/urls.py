from django.contrib import admin
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('thanks/<str:source>/', ThanksView.as_view(), name='thanks'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    # path('services/create/', service_create, name='service_create'),
    path("masters_services/", masters_services_by_id, name="masters_services_by_id_ajax"),
    path("order_create/", order_create, name="order_create"),
    path('review/create/', review_create, name='review_create'),
    path('masters/<int:master_id>/', MasterDetailView.as_view(), name='master_detail'),
    path('services/', ServicesListView.as_view(), name='services_list'),
    path("service_create/<str:form_mode>/", ServiceCreateView.as_view(), name="service_create"),
    path("service_update/<int:pk>", ServiceUpdateView.as_view(), name="service_update"),
]
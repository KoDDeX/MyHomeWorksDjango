from django.contrib import admin
from .models import Order, Service, Master, Review

# Register your models here.
admin.site.register(Order)
admin.site.register(Service)
admin.site.register(Master)
admin.site.register(Review)

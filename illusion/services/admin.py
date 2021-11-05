from django.contrib import admin

from .models import OrderHistory, Tag, Service

admin.site.register(OrderHistory)
admin.site.register(Tag)
admin.site.register(Service)

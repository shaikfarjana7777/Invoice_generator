from django.contrib import admin
from .models import Client, Invoice,InvoiceItem
# Register your models here.

admin.site.register(Client)
admin.register(Invoice)
admin.register(InvoiceItem)
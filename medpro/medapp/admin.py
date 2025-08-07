from django.contrib import admin
from.models import *
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
     list_display = ('name', 'card_number', 'expiry_date', 'amount', 'paid_at')
     search_fields = ('name', 'card_number')
     list_filter = ('paid_at',)
     admin.site.register(Demo)

# # Register your models here.

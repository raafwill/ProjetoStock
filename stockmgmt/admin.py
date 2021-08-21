from django.contrib import admin
from .forms import StockCreateForm

# Register your models here.
from .models import *


class StockCreateAdmin(admin.ModelAdmin):
   list_display = ['bebida', 'quantidade', 'preco_compra', 'data_recebimento']
   form = StockCreateForm
   list_filter = ['bebida', 'data_recebimento']
   search_fields = ['bebida']

admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Bebida)

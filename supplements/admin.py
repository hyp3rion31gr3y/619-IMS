from django.contrib import admin
from .models import Supplement, Sale

@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock_quantity', 'purchase_price', 'selling_price')
    list_editable = ('stock_quantity', 'selling_price')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('supplement', 'seller', 'quantity_sold', 'sale_date')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # If we passed ?supplement=ID in the URL, auto-select it
        if "supplement" in request.GET:
            form.base_fields['supplement'].initial = request.GET.get("supplement")
        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.seller = request.user
        super().save_model(request, obj, form, change)

# @admin.register(Sale)
# class SaleAdmin(admin.ModelAdmin):
#     list_display = ('supplement', 'seller', 'buyer_name', 'total_profit', 'sale_date')
#     readonly_fields = ('total_profit', 'seller') # Make seller read-only

#     def save_model(self, request, obj, form, change):
#         # Automatically set the seller to the currently logged-in user
#         if not obj.pk: # Only set it when the sale is first created
#             obj.seller = request.user
#         super().save_model(request, obj, form, change)
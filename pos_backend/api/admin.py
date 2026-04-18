from django.contrib import admin
from .models import Product, Inquiry, AuthAdmin

# Note: POS admin accounts are managed via the `createadmin` command.
# This creates both a Django superuser and an auth_admin table entry.


@admin.register(AuthAdmin)
class AuthAdminAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['name', 'email']
    readonly_fields = ['password', 'created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'mobile', 'product_name', 'created_at']
    search_fields = ['name', 'email']

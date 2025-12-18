# from django.contrib import admin
# # Register your models here.
# from .models import *


# admin.site.register(Service)


from django.contrib import admin
from .models import *

# admin.site.register(Category)
# admin.site.register(Service_category)
# admin.site.register(AddToCart)
# admin.site.register(AddToServiceCart)
# admin.site.register(Checkout)
# admin.site.register(Service_checkout)
# admin.site.register(OrderedServices)
# admin.site.register(OrderedProduct)
# Custom Admin for User model
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'is_customer', 'is_service', 'verified', 'gender', 'mobile_number', 'city')
    search_fields = ('username', 'email', 'name', 'mobile_number', 'city')
    list_filter = ('is_customer', 'is_service', 'verified', 'gender', 'city')
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email', 'name', 'profile_picture')
        }),
        ('Personal Info', {
            'fields': ('location', 'address', 'city', 'landmark', 'pincode', 'mobile_number', 'gender', 'date_of_birth')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'bank_account_number', 'ifsc_code', 'upi_id')
        }),
        ('Permissions', {
            'fields': ('is_customer', 'is_service', 'verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

# Custom Admin for Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'user')
    search_fields = ('product_name', 'category__name', 'user__username')
    list_filter = ('category', 'price')
    ordering = ('product_name',)
    fieldsets = (
        (None, {
            'fields': ('product_name', 'category', 'price', 'description', 'image', 'user')
        }),
    )

# Custom Admin for Service model
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'category', 'price', 'user')
    search_fields = ('service_name', 'category__name', 'user__username')
    list_filter = ('category', 'price')
    ordering = ('service_name',)
    fieldsets = (
        (None, {
            'fields': ('service_name', 'category', 'price', 'description', 'image', 'user')
        }),
    )

# Register the custom admin configurations
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)

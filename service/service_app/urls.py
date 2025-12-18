from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('services', views.services, name='services'),


    path('service_register', views.service_register, name='service_register'),
    path('service_login', views.service_login, name='service_login'),
    path('service_home', views.service_home, name='service_home'),
    path('service_logout', views.service_logout, name='service_logout'),
    path('manage_products', views.manage_products, name='manage_products'),
    path('manage_product_categories', views.manage_product_categories, name='manage_product_categories'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('manage_service_categories', views.manage_service_categories, name='manage_service_categories'),
    path('delete_service_category/<int:pk>/', views.delete_service_category, name='delete_service_category'),
    path('manage_services', views.manage_services, name='manage_services'),
    path('delete_service/<int:pk>/', views.delete_service, name='delete_service'),
    path('service_profile', views.service_profile, name='service_profile'),
    path('service_single/<int:pk>/', views.service_single, name='service_single'),
    path('products', views.products, name='products'),
    path('product_single/<int:pk>/', views.product_single, name='product_single'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),


    path('customer_login', views.customer_login, name='customer_login'),
    path('customer_register', views.customer_register, name='customer_register'),

    path('customer_logout', views.customer_logout, name='customer_logout'),
    path('product_cart', views.product_cart, name='product_cart'),
    path('update_cart_quantity', views.update_cart_quantity, name='update_cart_quantity'),
    path('product_remove_cart/<int:pk>/', views.product_remove_cart, name='product_remove_cart'),

    path('product_checkout', views.product_checkout, name='product_checkout'),
    path('payment_gateway/<int:pk>/', views.payment_gateway, name='payment_gateway'),
    path('order_placed', views.order_placed, name='order_placed'),
    path('customer_orders', views.customer_orders, name='customer_orders'),
    path('order_details/<int:pk>/', views.order_details, name='order_details'),
    path('manage_product_orders', views.manage_product_orders, name='manage_product_orders'),

    path('order_details_service_side/<int:order_id>/', views.order_details_service_side, name='order_details_service_side'),
    path('update_order_status/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),

    path('add_to_service_cart/<int:pk>/', views.add_to_service_cart, name='add_to_service_cart'),
    path('service_cart', views.service_cart, name='service_cart'),
    path('service_remove_cart/<int:pk>/', views.service_remove_cart, name='service_remove_cart'),
    path('service_checkout', views.service_checkout, name='service_checkout'),
    path('payment_gateway2/<int:pk>/', views.payment_gateway2, name='payment_gateway2'),
    path('service_orders', views.service_orders, name='service_orders'),
    path('service_order_details/<int:pk>/', views.service_order_details, name='service_order_details'),
    path('manage_service_requests', views.manage_service_requests, name='manage_service_requests'),
    path('service_details_service_side/<int:order_id>/', views.service_details_service_side, name='service_details_service_side'),
    path('update_service_status/<int:order_id>/update-status/', views.update_service_status, name='update_service_status'),



]
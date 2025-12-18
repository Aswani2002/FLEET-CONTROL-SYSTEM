from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import os
from django.conf import settings
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Create your views here.

def index(request):
    return render(request, 'general/index.html')

def services(request):
    services = Service.objects.all()
    context = {'services':services}
    return render(request, 'general/services.html', context)

def products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'general/products.html', context)

def service_single(request, pk):
    service = get_object_or_404(Service, pk=pk)
    context = {
        'service': service,
        'user': service.user  # passing the user who uploaded the service
    }
    return render(request, 'general/service_single.html', context)


def product_single(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'user': product.user  # passing the user who uploaded the service
    }
    return render(request, 'general/product_single.html', context)



# Service _center 

def service_register(request):
    if request.method == 'POST':
        service_center_name = request.POST.get('service_center')
        city = request.POST.get('city')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validation (you can extend this with more checks)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            try:
                # Create a new service center user
                user = User.objects.create(
                    name=service_center_name,
                    city=city,
                    email=email,
                    username=username,
                    is_service=True,
                    password=password, 
                )
                user.set_password(password)  # Hash the password
                user.save()  # Save the user with the hashed password


                # Optionally log the user in after registration
                # login(request, user)
                messages.success(request, 'Service center registered successfully!')
                return redirect('service_register')  # Redirect to success page or dashboard

            except IntegrityError:
                messages.error(request, 'An error occurred. Please try again.')

    return render(request, 'service_center/service_register.html')



def service_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_service:  # Check if the user is a service center user
                login(request, user)
                return redirect('service_home')  # Redirect to a service center dashboard or homepage
            else:
                messages.error(request, 'You are not registered as a service center user.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'service_center/service_login.html')



def service_home(request):
    return render(request, 'service_center/service_home.html')



@login_required
def service_profile(request):
    user = request.user

    if request.method == 'POST':
        # Updating editable fields directly from the POST request
        user.name = request.POST.get('name', user.name)
        user.location = request.POST.get('location', user.location)
        user.address = request.POST.get('address', user.address)
        user.city = request.POST.get('city', user.city)
        user.landmark = request.POST.get('landmark', user.landmark)
        user.pincode = request.POST.get('pincode', user.pincode)
        user.mobile_number = request.POST.get('mobile_number', user.mobile_number)
        user.bank_name = request.POST.get('bank_name', user.bank_name)
        user.bank_account_number = request.POST.get('bank_account_number', user.bank_account_number)
        user.ifsc_code = request.POST.get('ifsc_code', user.ifsc_code)
        user.upi_id = request.POST.get('upi_id', user.upi_id)

        # Handling profile picture upload
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']

        # Saving updated user details
        try:
            user.save()
            messages.success(request, 'Profile updated successfully!')
        except ValidationError as e:
            messages.error(request, f'Error updating profile: {e}')

        return redirect('service_profile')

    return render(request, 'service_center/service_profile.html', {'user': user})


def manage_products(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')  # Get the category ID from the form
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Handle image upload
        description = request.POST.get('description')

        # Ensure the user is logged in
        if request.user.is_authenticated:
            # Get only the categories uploaded by the logged-in user
            category = Category.objects.get(pk=category_id, user=request.user)
            product = Product(
                product_name=product_name,
                category=category,
                price=price,
                image=image,
                description=description,
                user=request.user
            )
            product.save()
            messages.success(request, "Product successfully created.")
            return redirect('manage_products')

    # Fetch products and categories for the logged-in user only
    products = Product.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'service_center/manage_products.html', context)



def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Optional: Ensure that the user can only delete their own products
    if product.user == request.user:
        product.delete()
        messages.success(request, "Product successfully deleted.")
    else:
        messages.error(request, "You are not authorized to delete this product.")

    return redirect('manage_products')

def manage_product_categories(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        user = request.user

        # Check if the category already exists for this user
        if Category.objects.filter(category_name=category_name, user=user).exists():
            messages.error(request, "Category already exists")
        else:
            # Create a new category
            Category.objects.create(category_name=category_name, user=user)
            messages.success(request, "Category successfully created")

        # Redirect back to the same page to display the message
        return redirect('manage_product_categories')

    # Retrieve categories for the current user to display in the table
    categories = Category.objects.filter(user=request.user)
    return render(request, 'service_center/manage_product_categories.html', {'categories': categories})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    # Optional: Ensure that the user can only delete their own categories
    if category.user == request.user:
        category.delete()
        messages.success(request, "Category successfully deleted.")
    else:
        messages.error(request, "You are not authorized to delete this category.")

    return redirect('manage_product_categories')



def manage_service_categories(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        user = request.user

        # Check if the category already exists for this user
        if Service_category.objects.filter(category_name=category_name, user=user).exists():
            messages.error(request, "Category already exists")
        else:
            # Create a new category
            Service_category.objects.create(category_name=category_name, user=user)
            messages.success(request, "Category successfully created")

        # Redirect back to the same page to display the message
        return redirect('manage_service_categories')

    # Retrieve categories for the current user to display in the table
    categories = Service_category.objects.filter(user=request.user)
    return render(request, 'service_center/manage_service_categories.html', {'categories': categories})


def delete_service_category(request, pk):
    category = get_object_or_404(Service_category, pk=pk)
    
    # Optional: Ensure that the user can only delete their own categories
    if category.user == request.user:
        category.delete()
        messages.success(request, "Category successfully deleted.")
    else:
        messages.error(request, "You are not authorized to delete this category.")

    return redirect('manage_service_categories')





def manage_services(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')  # Get the category ID from the form
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Handle image upload
        description = request.POST.get('description')

        # Ensure the user is logged in
        if request.user.is_authenticated:
            category = Service_category.objects.get(pk=category_id)
            product = Service(
                service_name=product_name,
                category=category,
                price=price,
                image=image,
                description=description,
                user=request.user
            )
            product.save()
            messages.success(request, "Service successfully created.")
            return redirect('manage_services')

    # Fetch all products and categories for the form
    products = Service.objects.filter(user=request.user)
    categories = Service_category.objects.filter(user=request.user)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'service_center/manage_services.html', context)



def delete_service(request, pk):
    product = get_object_or_404(Service, pk=pk)

    # Optional: Ensure that the user can only delete their own products
    if product.user == request.user:
        product.delete()
        messages.success(request, "Service successfully deleted.")
    else:
        messages.error(request, "You are not authorized to delete this service.")

    return redirect('manage_services')




def service_logout(request):
    logout(request)  # Logs out the user
    return redirect('index') 




def manage_product_orders(request):
    service_center_user = request.user  # Get the logged-in service center user

    # Fetch all the orders where products belong to the logged-in service center user
    orders = Checkout.objects.filter(ordered_products__product__user=service_center_user).distinct()

    context = {
        'orders': orders
    }
    return render(request, 'service_center/manage_product_orders.html', context)

def order_details_service_side(request, order_id):
    # Fetch order details for the specific order
    order = get_object_or_404(Checkout, id=order_id)
    ordered_products = order.ordered_products.all()

    context = {
        'order': order,
        'ordered_products': ordered_products,
    }
    return render(request, 'service_center/order_details_service_side.html', context)


def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Checkout, id=order_id)
        new_status = request.POST.get('status')
        
        # Update the order status
        order.status = new_status
        order.save()
        
        # Add a success message
        messages.success(request, 'Order status updated successfully.')
        
        return redirect('order_details_service_side', order_id=order_id)



###############################################################################
################################################################################
#Customer Login 



def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_customer:  # Check if the user is a service center user
                login(request, user)
                return redirect('index')  # Redirect to a service center dashboard or homepage
            else:
                messages.error(request, 'You are not registered as a user.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'customer/customer_login.html')



def customer_register(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validation (you can extend this with more checks)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            try:
                # Create a new service center user
                user = User.objects.create(
                    name=customer_name,
                    email=email,
                    username=username,
                    is_customer=True,
                    password=password, 
                )
                user.set_password(password)  # Hash the password
                user.save()  # Save the user with the hashed password


                # Optionally log the user in after registration
                # login(request, user)
                messages.success(request, 'account created successfully!')
                return redirect('customer_register')  # Redirect to success page or dashboard

            except IntegrityError:
                messages.error(request, 'An error occurred. Please try again.')

    return render(request, 'customer/customer_register.html')


def customer_logout(request):
    logout(request)  # Logs out the user
    return redirect('index') 




def add_to_cart(request, pk):
    user = request.user

    if user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)

        # Check if the product is in stock
        quantity = 1  # You can customize this based on your requirements
        price = product.price

            # Check if the product is already in the user's cart
        existing_cart_item = AddToCart.objects.filter(user=user, product=product).first()

        if existing_cart_item:
                # If the product is already in the cart, update the quantity
                existing_cart_item.quantity += quantity
                existing_cart_item.save()
        else:
                # If the product is not in the cart, create a new cart item
                cart_item = AddToCart(user=user, product=product, quantity=quantity, price=price)
                cart_item.save()

        messages.success(request, f"{product.product_name} added to your cart.")

        return redirect('products')  # Redirect to the cart page or any other page you want after adding to cart
 


 

from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages

# View for displaying the product cart
def product_cart(request):
    cart_items = AddToCart.objects.filter(user=request.user)
    allow_checkout = True
    same_shopkeeper = True
    shopkeepers = set()

    for cart_item in cart_items:
        cart_item.single_total = cart_item.product.price * cart_item.quantity
        cart_item.price = cart_item.product.price * cart_item.quantity
        cart_item.save()
        shopkeepers.add(cart_item.product.user)

    if len(shopkeepers) > 1:
        same_shopkeeper = False
        allow_checkout = False
        messages.warning(request, "Please select products from the same seller.")

    subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
    shipping_charge = 0  # Update based on logic
    total = subtotal + shipping_charge

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_charge': shipping_charge,
        'total': total,
        'allow_checkout': allow_checkout,
        'same_shopkeeper': same_shopkeeper,
    }
    return render(request, 'general/product_cart.html', context)


# View for updating cart quantity
def update_cart_quantity(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')

        cart_item = get_object_or_404(AddToCart, pk=cart_item_id)
        cart_item.quantity = int(quantity)
        cart_item.price = cart_item.product.price * cart_item.quantity
        cart_item.save()

        cart_items = AddToCart.objects.filter(user=request.user)
        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        total = subtotal  # Add shipping charge if applicable

        return JsonResponse({
            'single_total': cart_item.product.price * cart_item.quantity,
            'subtotal': subtotal,
            'total': total
        })
    return JsonResponse({'error': 'Invalid request method'})


# View for removing a product from the cart
def product_remove_cart(request, pk):
    cart_item = get_object_or_404(AddToCart, pk=pk)
    cart_item.delete()
    return redirect('product_cart')


@login_required
def product_checkout(request):
    if request.method == 'POST':
        cart_items = AddToCart.objects.filter(user=request.user)
        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        shipping_charge = 0
        total = subtotal + shipping_charge

        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        landmark = request.POST.get('landmark')
        msg = request.POST.get('bill')


        checkout_instance = Checkout.objects.create(
            user=request.user,
            total_price=total,
            address=address,
            city=city,
            pincode=pincode,
            landmark=landmark,
            status='Pending',
            message=msg,
            bank_name=None,  
            bank_acc_no=None,
            ifsc=None,
            cvv=None,
            paid=False
        )

        for cart_item in cart_items:
            OrderedProduct.objects.create(
                checkout=checkout_instance,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price
            )

        request.session['checkout_id'] = checkout_instance.pk  # Store checkout id in session

        return redirect('payment_gateway', pk=checkout_instance.pk)

    else:
        cart_items = AddToCart.objects.filter(user=request.user)
        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        shipping_charge = 0 
        total = subtotal + shipping_charge

        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_charge': shipping_charge,
            'total': total,
        }

        return render(request, 'general/product_checkout.html', context)


# @login_required
# def payment_gateway(request, pk):
#     checkout_instance = Checkout.objects.get(pk=pk)
#     context = {'checkout_instance':checkout_instance}
#     if request.method == 'POST':
#         # Assuming the form fields are named accordingly
#         bank_name = request.POST.get('bank_name')
#         bank_acc_no = request.POST.get('bank_acc_no')
#         ifsc = request.POST.get('ifsc')
#         cvv = request.POST.get('cvv')

#         # Update checkout instance with payment details
#         checkout_instance.bank_name = bank_name
#         checkout_instance.bank_acc_no = bank_acc_no
#         checkout_instance.ifsc = ifsc
#         checkout_instance.cvv = cvv
#         checkout_instance.paid = True
#         checkout_instance.save()

#         return redirect('order_placed')

#     return render(request, 'general/payment_gateway.html',context)
    
from decimal import Decimal

@login_required
def payment_gateway(request, pk):
    checkout_instance = Checkout.objects.get(pk=pk)

    context = {'checkout_instance': checkout_instance}
    
    if request.method == 'POST':
        # Assuming the form fields are named accordingly
        bank_name = request.POST.get('bank_name')
        bank_acc_no = request.POST.get('bank_acc_no')
        ifsc = request.POST.get('ifsc')
        cvv = request.POST.get('cvv')

        # Update checkout instance with payment details
        checkout_instance.bank_name = bank_name
        checkout_instance.bank_acc_no = bank_acc_no
        checkout_instance.ifsc = ifsc
        checkout_instance.cvv = cvv
        checkout_instance.paid = True
        checkout_instance.save()

        # Empty the cart after successful payment
        cart_items = AddToCart.objects.filter(user=request.user)
        cart_items.delete()

        return redirect('order_placed')

    return render(request, 'general/payment_gateway.html', context)




def order_placed(request):
    return render(request, 'general/order_placed.html')



@login_required
def customer_orders(request):
    orders = Checkout.objects.filter(user=request.user).order_by('-checkout_date')
    context = {
        'orders': orders,
    }
    return render(request, 'customer/customer_orders.html', context)

@login_required
def order_details(request, pk):
    order = get_object_or_404(Checkout, pk=pk, user=request.user)
    ordered_products = order.ordered_products.all()  # Get all products for the order
    context = {
        'order': order,
        'ordered_products': ordered_products,
    }
    return render(request, 'customer/order_details.html', context)




def add_to_service_cart(request, pk):
    user = request.user

    if user.is_authenticated:
        product = get_object_or_404(Service, pk=pk)

        price = product.price


        cart_item = AddToServiceCart(user=user, service=product, price=price)
        cart_item.save()

        messages.success(request, f"{product.service_name} added to your cart.")

        return redirect('services')  # Redirect to the cart page or any other page you want after adding to cart
 

def service_cart(request):
    cart_items = AddToServiceCart.objects.filter(user=request.user)
    allow_checkout = True
    same_shopkeeper = True
    shopkeepers = set()

    for cart_item in cart_items:
        cart_item.single_total = cart_item.service.price 
        cart_item.price = cart_item.service.price
        cart_item.save()
        shopkeepers.add(cart_item.service.user)

    if len(shopkeepers) > 1:
        same_shopkeeper = False
        allow_checkout = False
        messages.warning(request, "Please select products from the same seller.")

    subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
    shipping_charge = 0  # Update based on logic
    total = subtotal + shipping_charge

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_charge': shipping_charge,
        'total': total,
        'allow_checkout': allow_checkout,
        'same_shopkeeper': same_shopkeeper,
    }
    return render(request, 'general/service_cart.html', context)



def service_remove_cart(request, pk):
    cart_item = get_object_or_404(AddToServiceCart, pk=pk)
    cart_item.delete()
    return redirect('service_cart')



@login_required
def service_checkout(request):
    if request.method == 'POST':
        cart_items = AddToServiceCart.objects.filter(user=request.user)
        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        shipping_charge = 0
        total = subtotal + shipping_charge

        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        landmark = request.POST.get('landmark')
        msg = request.POST.get('bill')
        scheduled_date = request.POST.get('date')


        checkout_instance = Service_checkout.objects.create(
            user=request.user,
            total_price=total,
            address=address,
            city=city,
            pincode=pincode,
            landmark=landmark,
            status='Pending',
            scheduled_date = scheduled_date,
            message=msg,
            bank_name=None,  
            bank_acc_no=None,
            ifsc=None,
            cvv=None,
            paid=False
        )

        for cart_item in cart_items:
            OrderedServices.objects.create(
                checkout=checkout_instance,
                service=cart_item.service,
                price=cart_item.price
            )

        request.session['checkout_id'] = checkout_instance.pk  # Store checkout id in session

        return redirect('payment_gateway2', pk=checkout_instance.pk)

    else:
        cart_items = AddToServiceCart.objects.filter(user=request.user)
        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        shipping_charge = 0 
        total = subtotal + shipping_charge

        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_charge': shipping_charge,
            'total': total,
        }

        return render(request, 'general/service_checkout.html', context)



@login_required
def payment_gateway2(request, pk):
    checkout_instance = Service_checkout.objects.get(pk=pk)
    discount_price = checkout_instance.total_price * Decimal('0.2')

    context = {'checkout_instance': checkout_instance, 'discount_price':discount_price}
    
    if request.method == 'POST':
        # Assuming the form fields are named accordingly
        bank_name = request.POST.get('bank_name')
        bank_acc_no = request.POST.get('bank_acc_no')
        ifsc = request.POST.get('ifsc')
        cvv = request.POST.get('cvv')

        # Update checkout instance with payment details
        checkout_instance.bank_name = bank_name
        checkout_instance.bank_acc_no = bank_acc_no
        checkout_instance.ifsc = ifsc
        checkout_instance.cvv = cvv
        checkout_instance.paid = True
        checkout_instance.save()

        # Empty the cart after successful payment
        cart_items = AddToServiceCart.objects.filter(user=request.user)
        cart_items.delete()

        return redirect('order_placed')

    return render(request, 'general/payment_gateway2.html', context)

@login_required
def service_orders(request):
    orders = Service_checkout.objects.filter(user=request.user).order_by('-checkout_date')
    context = {
        'orders': orders,
    }
    return render(request, 'customer/service_orders.html', context)

@login_required
def service_order_details(request, pk):
    order = get_object_or_404(Service_checkout, pk=pk, user=request.user)
    ordered_products = order.ordered_products.all()  # Get all products for the order
    context = {
        'order': order,
        'ordered_products': ordered_products,
    }
    return render(request, 'customer/service_order_details.html', context)




def manage_service_requests(request):
    service_center_user = request.user  # Get the logged-in service center user

    # Fetch all the service orders where the services belong to the logged-in service center user
    orders = Service_checkout.objects.filter(ordered_products__service__user=service_center_user).distinct()

    context = {
        'orders': orders
    }
    return render(request, 'service_center/manage_service_requests.html', context)





def service_details_service_side(request, order_id):
    # Fetch order details for the specific order
    order = get_object_or_404(Service_checkout, id=order_id)
    ordered_products = order.ordered_products.all()

    context = {
        'order': order,
        'ordered_products': ordered_products,
    }
    return render(request, 'service_center/service_details_service_side.html', context)



def update_service_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Service_checkout, id=order_id)
        new_status = request.POST.get('status')
        
        # Update the order status
        order.status = new_status
        order.save()
        
        # Add a success message
        messages.success(request, 'Service status updated successfully.')
        
        return redirect('service_details_service_side', order_id=order_id)


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

from cart.cart import Cart
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages


@login_required(login_url='account:my-login')
def checkout(request):
    user = User.objects.get(id=request.user.id)
    if hasattr(user, 'user2shippingaddress'):
        # if user.user2shippingaddress:
        shipping_address = user.user2shippingaddress
    else:
        messages.info(request, 'Please add a shipping address')
        return redirect('account:manage-shipping')
    if not user.first_name:
        messages.info(request, 'Please complete your profile (First Name and Last Name)')
        return redirect('account:profile-management')
    context = {
        'shipping_address': shipping_address,
    }

    return render(request, 'payment/checkout.html', context)


def complete_order(request):
    user = request.user

    cart = Cart(request)
    total = cart.get_total()

    # Populate Order table
    order = Order.objects.create(
        full_name=user.first_name.capitalize() + ' ' + user.last_name.capitalize(),
        email=user.email,
        amount_paid=total,
        order2user=user,
    )
    for item in cart:
        OrderItem.objects.create(
            orderitem2order=order,
            orderitem2product=item['product'],
            quantity=item['qty'],
            price=item['price'],
            orderitem2user=user,
        )
    return JsonResponse({'redirect': '/payment/payment-success/'})


def payment_success(request):
    # Clear shopping cart
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]

    context = {}
    return render(request, 'payment/payment-success.html', context)


def payment_failed(request):
    context = {}
    return render(request, 'payment/payment-failed.html', context)

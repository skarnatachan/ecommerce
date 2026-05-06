from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payment.models import Order, OrderItem


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Email verification setup
            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string('account/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })
            user.email_user(
                subject=subject,
                message=message,
            )
            return redirect('account:email-verification-sent')

    context = {
        'form': form,
    }
    return render(request, 'account/registration/register.html', context)


def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('account:email-verification-success')
    else:
        return redirect('account:email-verification-failed')


def email_verification_sent(request):
    context = {}
    return render(request, 'account/registration/email-verification-sent.html', context)


def email_verification_success(request):
    context = {}
    return render(request, 'account/registration/email-verification-success.html', context)


def email_verification_failed(request):
    context = {}
    return render(request, 'account/registration/email-verification-failed.html', context)


def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('account:dashboard')
    context = {
        'form': form,
    }
    return render(request, 'account/my-login.html', context)


def user_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass

    messages.success(request, 'You have been logged out successfully')

    return redirect('store:store')


@login_required(login_url='account:my-login')
def dashboard(request):
    context = {}
    return render(request, 'account/dashboard.html', context)


@login_required(login_url='account:my-login')
def profile_management(request):
    form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('account:dashboard')
    context = {
        'form': form,
    }
    return render(request, 'account/profile-management.html', context)


@login_required(login_url='account:my-login')
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('store:store')
    context = {}
    return render(request, 'account/delete-account.html', context)


# Shipping Views
def manage_shipping(request):
    try:
        # Account User with shipment information
        shipping = ShippingAddress.objects.get(shippingaddress2user=request.user)
    except ShippingAddress.DoesNotExist:
        # Account user with no shipment information
        shipping = None
    form = ShippingForm(instance=shipping)
    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            shipping_user = form.save(commit=False)
            shipping_user.shippingaddress2user = request.user
            shipping_user.save()
            messages.success(request, 'Your shipping address has been updated successfully')
            return redirect('account:dashboard')
    context = {
        'form': form,
    }
    return render(request, 'account/manage-shipping.html', context)


@login_required(login_url='account:my-login')
def track_orders(request):
    orders = OrderItem.objects.filter(orderitem2user=request.user)

    context = {
        'orders': orders,
    }
    return render(request, 'account/track-orders.html', context)

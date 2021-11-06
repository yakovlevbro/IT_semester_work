from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm, CustomerForm, UserForm
from services.models import OrderHistory, Service
from django.contrib.auth.decorators import login_required




def reg_user(request):
    if request.user.is_authenticated:
        return redirect('customer_page')
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Acount was succesfully created')
            return redirect('login')
    context = {'form': form}
    return render(request, 'register_user.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('customer_page')
    form = LoginUserForm
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        remember_me = request.POST.get('remember_me')
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('customer_page')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {'form': form}
    return render(request, 'login_user.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def customer_page(request):
    customer_form = CustomerForm(instance=request.user.customer)
    user_form = UserForm(instance=request.user)
    orders = []
    for order in OrderHistory.objects.raw("select * from services_orderhistory "
                                            "where user_id=%s", [request.user.customer.id]):
        orders.append((Service.objects.get(pk=order.item_id), order.done_at))
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, instance=request.user.customer)
        user_form = UserForm(request.POST, instance=request.user)
        if customer_form.is_valid() and user_form.is_valid():
            customer_form.save()
            user_form.save()
            messages.success(request, "Данные обновлены")
    context = {'orderhistory': orders, 'form': customer_form, 'form_': user_form}
    return render(request, 'customer_page.html', context)
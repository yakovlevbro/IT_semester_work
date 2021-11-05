from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm



def reg_user(request):
    # if request.user.is_authenticated():
    #     return redirect('')
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Acount was succesfully created')
    context = {'form': form}
    return render(request, 'register_user.html', context)


def login_user(request):
    # if request.user.is_authenticated():
    #     return redirect('')
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
            # return redirect('')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {'form': form}
    return render(request, 'login_user.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')
import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ServiceForm, FeedbackForm
from .models import Service, OrderHistory, Feedback
from .decorators import allowed_users


def create_service(request):
    form = ServiceForm()
    context = {'form': form}
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Создание прошло успешно')
            return redirect('customer_page')
    return render(request, 'create_service.html', context)


@allowed_users(['admin'])
def update_service(request, pk):
    service = Service.objects.get(id=pk)
    form = ServiceForm(instance=service)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно сохранено')
    context = {'form': form}
    return render(request, 'create_service.html', context)


def search_page(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'search_page.html', context)


def service_page(request, pk):
    service = Service.objects.get(id=pk)
    customer = request.user.customer
    form = None
    if not Feedback.objects.filter(user=customer, item=service).exists():
        form = FeedbackForm()
    context = {'service': service, 'form': form}
    return render(request, 'service_page.html', context)



def create_order(request, pk):
    customer = request.user.customer
    service = Service.objects.get(id=pk)
    if OrderHistory.objects.filter(user=customer, item=service).filter(done_at=(datetime.datetime.now())).exists():
        messages.success(request, 'Вы уже заказали эту услугу!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if OrderHistory.objects.filter(user=customer).filter(done_at=(datetime.datetime.now())).count() < 3:
        order = OrderHistory(user=customer, item=service)
        order.save()
        messages.success(request, 'Благодарим за заявку, мы с вами скоро свяжемся!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.success(request, 'Вы превысили допустимое количество заказов на сегодня. Повторите попытку завтра.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

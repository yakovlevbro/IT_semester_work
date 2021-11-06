import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .forms import ServiceForm, FeedbackForm
from .models import Service, OrderHistory, Feedback, Tag
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

@allowed_users(['admin'])
@login_required(login_url='login')
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

@login_required(login_url='login')
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


@login_required(login_url='login')
def search_page(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'search_page.html', context)


@login_required(login_url='login')
def service_page(request, pk):
    service = Service.objects.get(id=pk)
    customer = request.user.customer

    feed = Feedback.objects.filter(item=service).exclude(user=customer)
    feed = Feedback.objects.filter(item=service, user=customer) | feed
    rating = None
    if Feedback.objects.filter(item=service).exists():
        rating = Feedback.objects.filter(item=service).aggregate(Avg('rating')).values()
        rating = int(list(rating)[0])
    tags = Tag.objects.filter(service=service)
    context = {'service': service, 'feed': feed, 'rating': rating, 'tags': tags}
    return render(request, 'service_page.html', context)


@login_required(login_url='login')
@allowed_users(['customer'])
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

@allowed_users(['customer'])
@login_required(login_url='login')
def create_feedback(request, pk):
    customer = request.user.customer
    service = Service.objects.get(id=pk)
    if OrderHistory.objects.filter(user=customer, item=service).exists():
        if not Feedback.objects.filter(user=customer, item=service).exists():
            instance = Feedback(user=customer, item=service)
            form = FeedbackForm(instance=instance)
        else:
            instance = Feedback.objects.get(user=customer, item=service)
            form = FeedbackForm(instance=instance)
    else:
        messages.success(request, 'Вы не можете оставлять отзывы на услуги, которые не заказывали')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'form': form}
    if request.method == 'POST':
        instance.text = request.POST.get('text')
        if request.POST.get('rating'):
            instance.rating = int(request.POST.get('rating'))
        else:
            instance.rating = 0
        instance.save()
        messages.success(request, 'Данные обновлены')
        return redirect('service_page', pk)
    return render(request, 'create_feedback.html', context)


@login_required(login_url='login')
def show_price(request):
    pk = request.GET.get('pk')
    if request.is_ajax():
        service = Service.objects.get(id=pk)
        price = service.price_ah
        return JsonResponse({'price': price}, status=200)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

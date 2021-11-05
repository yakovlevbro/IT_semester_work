from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ServiceForm
from .models import Service


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


def update_service(request, pk):
    service = Service.objects.get(id=pk)
    form = ServiceForm(instance=service)
    context = {'form': form}
    return render(request, 'create_service.html', context)

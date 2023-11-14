from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

from main.forms import loginForm


def index(request):

    context = {

    }

    return render(request, 'main/index.html', context)


def boxes_view(request):

    context = {

    }

    return render(request, 'main/boxes.html', context)


def faq_view(request):

    context = {

    }

    return render(request, 'main/faq.html', context)


def my_rent_view(request):
    context = {

    }

    return render(request, 'main/my-rent.html', context)


def my_rent_empty_view(request):
    context = {

    }

    return render(request, 'main/my-rent-empty.html', context)


def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            email=request.POST.get('EMAIL'),
            password=request.POST.get('PASSWORD')
        )
        if user is not None:
            login(request, user)
            context = {
                'user': user
            }
            return redirect(reverse('main:cabinet'), kwargs={})
        else:
            return HttpResponse('this user is not on site')

    else:
        return HttpResponse('Not POST method')


@login_required
def cabinet(request):

    if request.method == 'POST':
        email = request.POST.get('EMAIL')
        phone_number = request.POST.get('PHONE')
        password = request.POST.get('PASSWORD')
        first_name = request.POST.get('FIRSTNAME')
        last_name = request.POST.get('LASTNAME')
        user = request.user
        print(user)

        user.email = email
        user.phone_number = phone_number
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return render(request, 'main/my-rent.html', {})
    else:
        return render(request, 'main/my-rent.html', {})

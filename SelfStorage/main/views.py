from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

from main.models import Customer, Storage, Box, Rent, Status
from django.shortcuts import redirect, render
from django.urls import reverse
from main.models import Customer

from .tasks import send_email


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
def user_logout(request):
    logout(request)
    return render(request, 'main/index.html', {})


@login_required
def cabinet(request):

    if request.method == 'POST':
        email = request.POST.get('EMAIL_EDIT')
        phone_number = request.POST.get('PHONE_EDIT')
        first_name = request.POST.get('FIRSTNAME')
        last_name = request.POST.get('LASTNAME')
        user = request.user

        user.email = email
        user.phone_number = phone_number
        user.first_name = first_name
        user.last_name = last_name
        try:
            user.save()
            return render(request, 'main/my-rent.html', {})
        except IntegrityError as e:
            if 'unique constraint' in str(e.args).lower():
                context = {
                    'error': 'Такой телефон уже есть!'
                }
                return render(request, 'main/my-rent.html', context)
    else:

        storage_status = Status.objects.all().exclude(title='Хранение закончено')
        query = Q(renter=request.user) and Q(status__in=storage_status)
        rents = Rent.objects.filter(query).prefetch_related('renter').prefetch_related('box')

        my_rent = []
        for rent in rents:
            rent_item = {
                'renter': rent.renter,
                'box': rent.box,
                'start_date': rent.start_date,
                'end_date': rent.end_date,
                'status': rent.status,
                'delta': int((timezone.now().date() - rent.end_date).total_seconds()/86400)
            }
            my_rent.append(rent_item)

        context = {
            'my_rent': my_rent
        }

        return render(request, 'main/my-rent.html', context)


def close_box(request, box_id):

    box = get_object_or_404(Box, id=box_id)

    rent = get_object_or_404(Rent, box=box)

    close_status = get_object_or_404(Status, title='Хранение закончено')

    rent.status = close_status
    rent.save()

    query = Q(renter=request.user) and Q(status__id=5)
    rents = Rent.objects.filter(query).prefetch_related('renter').prefetch_related('box')

    my_rent = []
    for rent in rents:
        rent_item = {
            'renter': rent.renter,
            'box': rent.box,
            'start_date': rent.start_date,
            'end_date': rent.end_date,
            'status': rent.status,
            'delta': int((timezone.now().date() - rent.end_date).total_seconds() / 86400)
        }
        my_rent.append(rent_item)

    context = {
        'my_rent': my_rent
    }
    return render(request, 'main/my-rent.html', context)


def continue_rent(request):
    if request.method == 'POST':
        new_date = datetime.datetime.strptime(request.POST.get('TO_DATE'), "%Y-%m-%d").date()
        box = get_object_or_404(Box, pk=request.POST.get('BOX_ID'))

        rent = get_object_or_404(Rent, box=box)

        rent.end_date = new_date
        rent.save()

        storage_status = Status.objects.all().exclude(title='Хранение закончено')
        query = Q(renter=request.user) and Q(status__in=storage_status)
        rents = Rent.objects.filter(query).prefetch_related('renter').prefetch_related('box')

        my_rent = []
        for rent in rents:
            rent_item = {
                'renter': rent.renter,
                'box': rent.box,
                'start_date': rent.start_date,
                'end_date': rent.end_date,
                'status': rent.status,
                'delta': int((timezone.now().date() - rent.end_date).total_seconds() / 86400)
            }
            my_rent.append(rent_item)

        context = {
            'my_rent': my_rent
        }

        return render(request, 'main/my-rent.html', context)

    else:
        storage_status = Status.objects.all().exclude(title='Хранение закончено')
        query = Q(renter=request.user) and Q(status__in=storage_status)
        rents = Rent.objects.filter(query).prefetch_related('renter').prefetch_related('box')

        my_rent = []
        for rent in rents:
            rent_item = {
                'renter': rent.renter,
                'box': rent.box,
                'start_date': rent.start_date,
                'end_date': rent.end_date,
                'status': rent.status,
                'delta': int((timezone.now().date() - rent.end_date).total_seconds() / 86400)
            }
            my_rent.append(rent_item)

        context = {
            'my_rent': my_rent
        }
        return render(request, 'main/my-rent.html', context)


def user_registration(request):

    if request.method == 'POST':
        email = request.POST.get('EMAIL_CREATE')
        first_name = request.POST.get('FIRSTNAME_CREATE')
        last_name = request.POST.get('LASTNAME_CREATE')
        phone = request.POST.get('PHONE_CREATE')
        password_create = request.POST.get('PASSWORD_CREATE')
        password_confirm = request.POST.get('PASSWORD_CONFIRM')
        if password_create == password_confirm:
            user = Customer.objects.create_user(
                email=email,
                password=password_create,
                name=f'{first_name} {last_name}',
                phone_number=phone,
                first_name=first_name,
                last_name=last_name,
                is_read_pd=True
            )
            login(request, user)
            return redirect(reverse('main:cabinet'), kwargs={})
        else:
            messages.add_message(request, messages.WARNING, 'Введенные пароли не совпадают!')
            next = request.POST.get('next', '/')
            context = {
                'error': 'Введенные пароли не совпадают!'
            }
            return HttpResponseRedirect(next, context)

    else:
        return render(request, 'main/index.html', {})


def contacts(request):
    send_email.delay('vladpap@mail.ru')
    context = {

    }
    return render(request, 'main/contacts.html', context)


def law_doc(request):

    context = {

    }
    return render(request, 'main/law_doc.html', context)


def policy(request):

    context = {

    }
    return render(request, 'main/policy.html', context)


def tariff(request):

    context = {

    }
    return render(request, 'main/tariff.html', context)


def calc(request):

    context = {

    }
    return render(request, 'main/calc.html', context)


def feedbacks(request):

    context = {

    }
    return render(request, 'main/feedbacks.html', context)


def storage_list(request):

    context = {

    }
    return render(request, 'main/storage_list.html', context)


def agreement(request):
    context = {

    }
    return render(request, 'main/agreement.html', context)


def forget_password(request):
    context = {

    }
    return render(request, 'main/forget_password.html', context)


def order(request):
    context = {

    }
    return render(request, 'main/order.html', context)

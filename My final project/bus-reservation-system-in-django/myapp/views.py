from django.shortcuts import render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Bus, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings




def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from .models import Bus

@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source', '').strip()
        dest_r = request.POST.get('destination', '').strip()
        date_r = request.POST.get('date', '').strip()

        try:
            date_obj = datetime.strptime(date_r, '%Y-%m-%d').date()
        except ValueError:
            context["error"] = "Invalid date format."
            return render(request, 'myapp/findbus.html', context)

        weekday = date_obj.strftime('%A').lower()  # e.g. 'thursday'
        date_field = f"{weekday}_date"
        time_field = f"{weekday}_time"

        filter_kwargs = {
            'source': source_r,
            'dest': dest_r,
            f'{date_field}': date_obj
        }

        bus_list = Bus.objects.filter(**filter_kwargs)

        # Inject matched date and time for template display
        for bus in bus_list:
            setattr(bus, 'date', getattr(bus, date_field))
            setattr(bus, 'time', getattr(bus, time_field))

        if bus_list:
            return render(request, 'myapp/list.html', {'bus_list': bus_list})
        else:
            context["error"] = "Sorry, no buses available."
            return render(request, 'myapp/findbus.html', context)

    return render(request, 'myapp/findbus.html')

@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        date_r = request.POST.get('date')

        try:
            date_obj = datetime.strptime(date_r, '%Y-%m-%d').date()
        except Exception:
            context["error"] = "Invalid date format."
            return render(request, 'myapp/findbus.html', context)

        weekday = date_obj.strftime('%A').lower()
        date_field = f"{weekday}_date"
        time_field = f"{weekday}_time"

        bus = Bus.objects.get(id=id_r)

        setattr(bus, 'date', getattr(bus, date_field))
        setattr(bus, 'time', getattr(bus, time_field))

        if bus.rem >= seats_r:
            name_r = bus.bus_name
            cost = seats_r * bus.price
            source_r = bus.source
            dest_r = bus.dest
            price_r = bus.price
            username_r = request.user.username
            email_r = request.user.email
            userid_r = request.user.id
            rem_r = bus.rem - seats_r
            Bus.objects.filter(id=id_r).update(rem=rem_r)

            book = Book.objects.create(
                name=username_r,
                email=email_r,
                userid=userid_r,
                bus_name=name_r,
                source=source_r,
                busid=id_r,
                dest=dest_r,
                price=price_r,
                nos=seats_r,
                date=bus.date,
                time=bus.time,
                status='BOOKED'
            )

            # Send confirmation email
            subject = 'Bus Booking Confirmation'
            message = f"""
Dear {book.name},

Your booking is confirmed!

Bus Name: {book.bus_name}
Source: {book.source}
Destination: {book.dest}
Number of seats booked: {book.nos}
Date: {book.date}
Time: {book.time}
Total cost: {cost}


Thank you for choosing GaTravel Bus Reservation.
"""
            recipient_list = [book.email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

            return render(request, 'myapp/bookings.html', {
                'book': book,
                'cost': cost,
            })
        else:
            context["error"] = "Sorry, select fewer number of seats"
            return render(request, 'myapp/findbus.html', context)

    return render(request, 'myapp/findbus.html')

@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'myapp/findbus.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)

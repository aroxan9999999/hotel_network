import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.edit import BaseCreateView

from _stripe_.utils import __send_email as send_mail_to
from .models import *
from django.views.generic import ListView, DetailView, TemplateView

User = get_user_model()


class Index_view(ListView):
    model = Hotel
    template_name = "index.html"
    context_object_name = 'hotel_object'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'lagoona'
        context['service_object'] = Service.objects.all()
        context["spec_offers"] = Tour.objects.select_related('hotel').filter(place__gte=1)
        return context

    def post(self, request, *args, **kwargs):
        form = self.request.POST
        country = form.get('country')
        date = form.get('date')
        nights = int(form.get('nights'))
        tourist = int(form.get('tourist'))
        fly = form.get('fly')
        tour_title = form.get("tour")
        tour = Tour.objects.filter(title=tour_title, place__gte=tourist)
        # user = self.request.user
        user = User.objects.get(username=form.get('username'))  # from test user
        if not tour.exists():
            content = 'недостоточно мест'
            tour = Tour.objects.get(title=tour_title)
            send_mail_to(to=user.email, content=content, subject=f'недостаточно место {tour.hotel.name}')
            return redirect('tour_detail', pk=tour.pk)
        tour = tour[0]
        price = tour.price
        all_price = price * (tourist * nights)
        many = user.many
        if many < all_price:
            content = f'низкий баланс не хватает {all_price - user.many} $'
            send_mail_to(to=user.email, content=content, subject=f'Payment small balance {tour.hotel.name}')
            return redirect('payments')
        many -= all_price
        user.billet.active = True
        user.billet.price = all_price
        user.billet.hotel = tour.hotel
        user.billet.numbers_person = tourist
        user.billet.billet_time_start = date
        date = [int(date) for date in date.split('-')]
        user.billet.billet_time_end = datetime.datetime(day=date[2], year=date[0],
                                                        month=date[1]).today() + datetime.timedelta(days=nights)
        tour.place -= tourist
        if tour.place == 0:
            tour.active = False
        user.save()
        user.billet.save()
        tour.save()
        content = f'''ваш билет куплен !!! потрачено {"{0:,}".format(all_price).replace(',', ' ')} $'''
        send_mail_to(to=user.email, content=content, subject=f'ваш билет куплен {tour.hotel.name}')
        return redirect("/")

    def get_queryset(self):
        return Hotel.objects.all()


class Show_detail(DetailView):
    context_object_name = 'hotel'
    template_name = 'detail.html'
    model = Hotel

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['hotel'].name
        context['count'] = context['hotel'].get_hotel_object.filter(active=True).count
        context['object_list'] = context['hotel'].get_hotel_object.filter(active=True)
        return context


class NumberDetail(DetailView):
    template_name = 'numbers_detail.html'
    model = Hotel_number

    def post(self, request, *args, **kwargs):
        number = Hotel_number.objects.get(pk=self.kwargs.get("pk"))
        # user = self.request.user
        user = User.objects.get(username=self.request.POST.get("username"))  # for testing
        if user.many < number.price:
            content = f'низкий баланс не хватает {number.price - user.many} $'
            send_mail_to(to=user.email, content=content, subject=f'Payment small balance {number.hotel.name}')
            return redirect('payments')
        user.many -= number.price
        user.number.active = True
        user.number.price = number.price
        user.number.hotel = number.hotel
        number.bronny = True
        number.active = False
        user.number.save()
        number.save()
        user.save()
        content = f"поздравлаем вы забронировали номер "
        send_mail_to(to=user.email, content=content, subject=f'Payment book to hotel {number.hotel.name}')
        return redirect("/")


class Spec_detail(TemplateView):
    template_name = 'spec_detail.html'
    context_object_name = 'service'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'tour'
        print(context['title'])
        context['object_list'] = Tour.objects.filter(active=True, place__gte=1)
        context['count'] = context['object_list'].count
        return context


class Tour_detail(TemplateView):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Tour.objects.get(pk=self.kwargs.get('pk'))
        return context

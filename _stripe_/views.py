from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
import stripe
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from .utils import __send_email as send_mail_to


User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY
price_dict = {}


class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        price = int(request.POST.get('payment'))
        price_dict[str(self.request.user.email)] = price
        print(price_dict)
        cents = price * 100
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {'unit_amount': cents, 'currency': 'USD',
                                   'product_data': {
                                       'name': f'pyment to {self.request.user.username}',
                                   }
                                   },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/payment/success',
            cancel_url='http://127.0.0.1:8000/',
        )
        return redirect(checkout_session.url, code=303)


class PymentView(TemplateView):
    pass


class SuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        print(price_dict)
        price = price_dict[str(self.request.user.email)]
        context = super().get_context_data(**kwargs)
        context['title'] = 'success'
        context['price'] = '{0:,}'.format(price).replace(',', ' ')
        user = User.objects.get(username=self.request.user.username)
        user.many += price
        user.save()
        many = '{0:,}'.format(self.request.user.many + price).replace(',', ' ')
        context['many'] = many
        content = f'''<h1>Payment successfully</h1>
                     <h2>Ваш баланс {many} $</h2>
                     <h3>паполнено {price} $</h3>'''
        send_mail_to(to=self.request.user.email, content=content, subject="Payment Succesfully")
        return context

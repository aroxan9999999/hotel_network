from django.urls import path, include
from .views import CreateCheckoutSession, PymentView, SuccessView

urlpatterns = [
    path('session/', CreateCheckoutSession.as_view(), name='session'),
    path('', PymentView.as_view(template_name='payments.html'), name='payments'),
    path('success', SuccessView.as_view(), name='success'),

]

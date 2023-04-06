from django.urls import path, include
from .views import Index_view, Show_detail, NumberDetail, Spec_detail, Tour_detail

urlpatterns = [
    path('', Index_view.as_view(), name='index'),
    path('<int:pk>', Show_detail.as_view(), name='detail'),
    path('spec', Spec_detail.as_view(), name='spec_detail'),
    path('number/<int:pk>', NumberDetail.as_view(), name='number_detail'),
    path('tour/<int:pk>', Tour_detail.as_view(template_name='spec_tour_detail.html'), name='tour_detail'),
]

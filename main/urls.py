from django.urls import path , include
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('payment', views.payment_start, name='payment_start'),
    path('payment/return', views.payment_return, name='payment_return'),
    path('payment/check/<pk>', views.payment_check, name='payment_check'),
    path('requirement', views.requirement, name='requirement'),
    path('about-me', views.about_me, name='about_me'),
]
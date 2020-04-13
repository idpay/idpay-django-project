from django.urls import path , include
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('start', views.start_payment, name='start_payment'),
    path('verify', views.payment_verify, name='payment_verify'),
    path('requirement', views.requirement, name='requirement'),
    path('about_me', views.about_me, name='about_me'),
    path('payment/check/<pk>', views.payment_check, name='payment_check'),
]
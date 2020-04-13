from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from django.views.decorators.csrf import csrf_exempt

import zeep
from zeep import Client
import requests
import json

api = 'your api key here!'


def home(request):
    payments = Main.objects.all()
    return render(request, 'home.html', {'payments': payments})


def start_payment(request):
    if request.method == 'POST':

        amount = request.POST.get('amount')

        url = 'https://api.idpay.ir/v1.1/payment'
        orderid = '123456'
        callbackurl = 'yourdomain.com/verify'

        data = {'order_id': orderid, 'amount': amount, 'callback': callbackurl}
        headers = {'Content-Type': 'application/json', 'X-API-KEY': api, 'X-SANDBOX': '1'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        if r.status_code == 201:

            e = r.json()
            link = e['link']
            pid = e['id']

            b = Main(payment_id=pid, amount=int(amount))
            b.save()

            return redirect(link)

        else:

            e = r.json()
            txt = "Error Code : " + str(r.status_code) + "   |   " + "Description : " + str(e['error_message'])

    else:
        txt = "Bad Request"

    return render(request, 'error.html', {'txt': txt})


@csrf_exempt
def payment_verify(request):
    if request.method == 'POST':

        status = request.POST.get('status')
        pidtrack = request.POST.get('track_id')
        pid = request.POST.get('id')
        amount = request.POST.get('amount')
        card = request.POST.get('card_no')
        date = request.POST.get('date')

        if Main.objects.filter(payment_id=pid, amount=amount).count() == 1:

            b = Main.objects.get(payment_id=pid, amount=amount)
            b.status = status
            b.date = str(date)
            b.card_number = card
            b.idpay_track_id = pidtrack
            b.save()

            if str(status) == '10':

                url = 'https://api.idpay.ir/v1.1/payment/verify'

                orderid = '123456'

                data = {'order_id': orderid, 'id': pid}
                headers = {'Content-Type': 'application/json', 'X-API-KEY': api, 'X-SANDBOX': '1'}
                r = requests.post(url, data=json.dumps(data), headers=headers)

                if r.status_code == 200:

                    e = r.json()

                    b = Main.objects.get(payment_id=pid, amount=amount)
                    b.status = e['status']
                    b.bank_track_id = e['payment']['track_id']
                    b.save()

                    txt = "Transaction Verified"
                    return render(request, 'error.html', {'txt': txt})

                else:

                    e = r.json()
                    txt = "Error Code : " + str(r.status_code) + "   |   " + "Description : " + str(e['error_message'])

            else:

                if str(status) == '1':
                    txt = "Error Code : " + str(status) + "   |   " + "Description : " + "پرداخت انجام نشده"
                elif str(status) == '2':
                    txt = "Error Code : " + str(status) + "   |   " + "Description : " + "پرداخت نا موفق"
                elif str(status) == '3':
                    txt = "Error Code : " + str(status) + "   |   " + "Description : " + "خطایی رخ داده"
                elif str(status) == '6':
                    txt = "Error Code : " + str(status) + "   |   " + "Description : " + "برگشت خورده سیستمی"

        else:

            txt = "Bad Request"

    else:

        txt = "Bad Request"

    return render(request, 'error.html', {'txt': txt})


def payment_check(request, pk):
    url = 'https://api.idpay.ir/v1.1/payment/inquiry'
    orderid = '123456'

    pid = Main.objects.get(pk=pk).payment_id

    data = {'order_id': orderid, 'id': pid}
    headers = {'Content-Type': 'application/json', 'X-API-KEY': api, 'X-SANDBOX': '1'}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    if r.status_code == 200:

        e = r.json()
        txt = "Status Code : " + str(e.get('status'))

    else:

        e = r.json()
        txt = "Error Code : " + str(r.status_code) + "   |   " + "Description : " + str(e['error_message'])

    return render(request, 'error.html', {'txt': txt})


def requirement(request):
    txt = "pip install zeep"

    return render(request, 'error.html', {'txt': txt})


def about_me(request):
    txt = 'IDPay'

    return render(request, 'error.html', {'txt': txt})

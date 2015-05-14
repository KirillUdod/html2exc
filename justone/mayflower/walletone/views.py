#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from walletone.forms import WalletoneResultForm
from walletone.models import PaymentNotification
from walletone.signals import payment_received


@csrf_exempt
def receive_result(request):
    form = WalletoneResultForm(request.POST)

    if form.is_valid():
        order_id = form.cleaned_data['WMI_PAYMENT_NO']
        amount = form.cleaned_data['WMI_PAYMENT_AMOUNT']
        merchant_order_id = form.cleaned_data['WMI_ORDER_ID']

        # сохраняем данные об успешном платеже в базе
        notification = PaymentNotification.objects.create(order_id=order_id, amount=amount,
                                                          merchant_order_id=merchant_order_id)

        payment_received.send(sender=notification, order_id=order_id, amount=amount,
                              merchant_order_id=merchant_order_id)

    return HttpResponse(form.get_result_string())


@csrf_exempt
def success_view(request, template_name='walletone/success.html', extra_context=None):
    context = {}
    context.update(extra_context or {})

    return render(request, template_name, context)


@csrf_exempt
def fail_view(request, template_name='walletone/fail.html', extra_context=None):
    context = {}
    context.update(extra_context or {})

    return render(request, template_name, context)
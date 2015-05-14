#coding: utf-8
from django.dispatch import Signal

payment_received = Signal(providing_args=['order_id', 'merchant_order_id', 'amount'])


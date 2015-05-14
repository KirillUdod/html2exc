#coding: utf-8

from django.conf import settings

# обязательные параметры - реквизиты магазина
MERCHANT_ID = settings.WALLETONE_MERCHANT_ID

USE_SIGNATURE = getattr(settings, 'WALLETTONE_USE_SIGNATURE', False)

if USE_SIGNATURE:
    SIGNATURE = settings.WALLETTONE_SIGNATURE
else:
    SIGNATURE = ''

FORM_TARGET = u'https://www.walletone.com/checkout/'

AMOUNTS = {
    'RUR': 643,  # 643 — Российские рубли
    'EUR': 978,  # 978 — Евро
    'USD': 840  # 840 — Американские доллары
}

# 710 — Южно-Африканские ранды
# 980 — Украинские гривны
# 398 — Казахстанские тенге
# 974 — Белорусские рубли
# 972 — Таджикские сомони
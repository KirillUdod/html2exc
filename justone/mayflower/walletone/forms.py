#coding: utf-8
from hashlib import md5
from urllib import urlencode, quote, quote_plus
from base64 import b64encode
import binascii

from django import forms
from django.core.urlresolvers import reverse

from walletone.conf import MERCHANT_ID, SIGNATURE, AMOUNTS, FORM_TARGET, USE_SIGNATURE
# from robokassa.models import SuccessNotification


class WalletoneBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(WalletoneBaseForm, self).__init__(*args, **kwargs)

    def _get_signature(self):
        str_buff = ''
        if not self.data:
            for field_name in sorted(self.fields.iterkeys(), key=lambda s: unicode(s).lower()):
                initial = self._get_initial(field_name, self.fields[field_name])
                # print 'field_name', field_name, 'initial', initial

                if initial:
                    str_buff += initial
        else:
            for field_name in sorted(self.data.iterkeys(), key=lambda s: unicode(s).lower()):
                if field_name != 'WMI_SIGNATURE':
                    post_val = unicode(self.data.get(field_name, '')).encode('1251')
                    # print 'field_name', field_name, 'post_val', repr(post_val)
                    str_buff += post_val

        res = b64encode(md5(str_buff + SIGNATURE).digest())
        # print 'str_buff', str_buff
        # print 'res', res
        return res

    def _get_initial(self, name, field):
        val = self.initial.get(name, field.initial)

        if val:
            if isinstance(val, unicode):
                val = 'BASE64:%s' % b64encode(unicode(val).encode('utf8'))
            else:
                val = unicode(val).encode('1251')

        return val

    def clean_WMI_SIGNATURE(self):
        return self._get_signature()


class WalletonePaymentForm(WalletoneBaseForm):
    # login магазина в обменном пункте
    WMI_MERCHANT_ID = forms.IntegerField(initial=MERCHANT_ID)
    WMI_PAYMENT_AMOUNT = forms.DecimalField()
    WMI_CURRENCY_ID = forms.IntegerField(initial=AMOUNTS['RUR'])
    WMI_PAYMENT_NO = forms.IntegerField()
    WMI_DESCRIPTION = forms.CharField(required=False)
    WMI_SUCCESS_URL = forms.CharField()
    WMI_FAIL_URL = forms.CharField()

    def __init__(self, *args, **kwargs):
        host = kwargs.pop('host')
        protocol = kwargs.pop('protocol', 'http')

        super(WalletonePaymentForm, self).__init__(*args, **kwargs)

        self.fields['WMI_SUCCESS_URL'].initial = '%s://%s%s' % (protocol, host, reverse('walletone_success'))
        self.fields['WMI_FAIL_URL'].initial = '%s://%s%s' % (protocol, host, reverse('walletone_fail'))

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        if USE_SIGNATURE:
            self.fields['WMI_SIGNATURE'] = forms.CharField(max_length=24, initial=self._get_signature())

    def get_redirect_url(self):
        """ Получить URL с GET-параметрами, соответствующими значениям полей в
        форме. Редирект на адрес, возвращаемый этим методом, эквивалентен
        ручной отправке формы методом GET.
        """
        params = []

        for name, field in self.fields.iteritems():
            value = self._get_initial(name, field)
            if value:
                params.append('%s=%s' % (name, quote_plus(value)))

        # TODO urlencode params
        return FORM_TARGET + '?' + '&'.join(params)


class WalletoneResultForm(WalletoneBaseForm):
    """
    Форма для приема результатов платежа и проверки контрольной суммы
    """
    WMI_PAYMENT_AMOUNT = forms.DecimalField(label=u'Сумма заказа')
    WMI_PAYMENT_NO = forms.IntegerField(label=u'Идентификатор заказа в системе учета интернет-магазина', min_value=0)
    WMI_ORDER_ID = forms.IntegerField(label=u'Идентификатор заказа в системе учета Единой кассы', min_value=0)

    # присылаются системой, но не используются нигде
    WMI_CURRENCY_ID = forms.CharField(label=u'Идентификатор валюты заказа (ISO 4217)', )
    WMI_MERCHANT_ID = forms.CharField(label=u'Идентификатор (номер кошелька) интернет-магазина', required=False)
    WMI_UPDATE_DATE = forms.CharField(required=False)
    WMI_CREATE_DATE = forms.CharField(required=False)
    WMI_FAIL_URL = forms.CharField(required=False)
    WMI_NOTIFY_COUNT = forms.CharField(required=False)
    WMI_AUTO_ACCEPT = forms.CharField(required=False)
    WMI_ORDER_STATE = forms.CharField(required=False)
    WMI_SUCCESS_URL = forms.CharField(required=False)
    WMI_DESCRIPTION = forms.CharField(required=False)
    WMI_LAST_NOTIFY_DATE = forms.CharField(required=False)
    WMI_EXTERNAL_ACCOUNT_ID = forms.CharField(required=False)
    WMI_PAYMENT_TYPE = forms.CharField(required=False)
    WMI_EXPIRED_DATE = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(WalletoneResultForm, self).__init__(*args, **kwargs)

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        if USE_SIGNATURE:
            self.fields['WMI_SIGNATURE'] = forms.CharField(max_length=24)

    def clean(self):
        if USE_SIGNATURE:
            try:
                signature = self.cleaned_data['WMI_SIGNATURE'].lower()
                if signature != self._get_signature().lower():
                    raise forms.ValidationError(u'Неверная контрольная сумма')
            except KeyError:
                raise forms.ValidationError(u'Пришли не все необходимые параметры')

        return self.cleaned_data

    def get_result_string(self, error_description=''):
        if self.is_valid():
            return 'WMI_RESULT=OK'
        else:
            return 'WMI_RESULT=RETRY%s' % (('&WMI_DESCRIPTION=%s' % unicode(error_description).encode('1251'))
                                           if error_description else '')
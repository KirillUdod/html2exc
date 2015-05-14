#coding:utf8
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError

from mayflower.forms import PlaceholderForm
from order.const import ADD_TOY_PRICE, DELIVERY_TYPES, FREE_DELIVERY_PRICE, ORDER_MINIMAL_PRICE
from order.models import Order, ORDER_CLARIFY_NO_PHONE, ORDER_CLARIFY_PHONE
from order.widgets import ExtRadioSelect


class OrderForm(PlaceholderForm, forms.ModelForm):
    accept_terms = forms.BooleanField(label=u'Я принимаю условия доставки', initial=True,
                                      error_messages={'required': u'Необходимо принять условия доставки'})

    class Meta:
        model = Order
        exclude = ['unique_hash', 'order_price', 'is_paid', 'delivery_time', 'delivery_price',
                   'positions', 'date', 'pay_type_old']
        widgets = {
            'pay_type': ExtRadioSelect(attrs={'id': 'pay_type'}),
            'clarify_type': ExtRadioSelect(attrs={'id': 'clarify_type'}),
            'add_card': ExtRadioSelect(attrs={'id': 'add_card'}),
        }

    def __init__(self, *args, **kwargs):
        self.basket_summary = kwargs.pop('basket_summary')
        self.delivery_today = False

        super(OrderForm, self).__init__(*args, **kwargs)

        if self.basket_summary < ADD_TOY_PRICE:
            self.fields['add_toy'].widget.attrs.update({'disabled': ''})

        # tmp_disables = {'disabled': '', 'rel': 'error'}
        tmp_disables = {'disabled': ''}

        self.fields['destination_address'].required = True
        self.fields['destination_name'].required = True
        self.fields['destination_phone'].required = True

        if self.is_bound:
            if self.data.get('phone_only') == 'on':
                self.fields['destination_address'].required = False
                self.fields['destination_name'].required = False
                self.fields['destination_phone'].required = True

                if self.data.get('customer_is_destination') == 'on':
                    self.data['customer_is_destination'] = 'off'
            else:
                if self.data.get('anonymous_delivery') == 'on':
                    if self.data.get('customer_is_destination') == 'on':
                        self.data['customer_is_destination'] = 'off'

            #
            if self.data.get('customer_is_destination') == 'on':
                self.fields['destination_name'].required = False
                self.fields['destination_phone'].required = False

                if self.data.get('anonymous_delivery') == 'on':
                    self.data['anonymous_delivery'] = 'off'

                if self.data.get('phone_only') == 'on':
                    self.data['phone_only'] = 'off'
            # else:
                # if int(self.data.get('clarify_type')) != ORDER_CLARIFY_NO_PHONE:
                #     self.fields['destination_phone'].required = True

            #
            if self.data.get('pay_type') == 'nalk' or self.data.get('customer_is_destination') == 'on':
                if int(self.data.get('clarify_type', 0)) == ORDER_CLARIFY_NO_PHONE:
                    self.data['clarify_type'] = ORDER_CLARIFY_PHONE

                if self.data.get('make_photo') == 'on':
                    self.data['make_photo'] = False

                if self.data.get('send_sms') == 'on':
                    self.data['send_sms'] = False

    def clean(self):
        if not self.basket_summary:
            raise ValidationError(u'Вы еще не добавили ни одного товара в корзину')
        elif self.basket_summary < ORDER_MINIMAL_PRICE:
            raise ValidationError(u'Минимальная сумма заказа %s рублей' % ORDER_MINIMAL_PRICE)

        if self.basket_summary < ADD_TOY_PRICE and self.cleaned_data.get('add_toy'):
            raise ValidationError(u'Мягкую игрушку можно добавить только при заказе свыше %s рублей' % ADD_TOY_PRICE)

        if self.cleaned_data.get('pay_type') == 'nal' and\
            (not self.cleaned_data.get('pay_for_delivery_date') or not self.cleaned_data.get('pay_for_delivery_time')
             or not self.cleaned_data.get('pay_for_delivery_address')):
            raise ValidationError(u'При выборе выезда курьера за оплатой необходимо указать дату, время и адрес'
                                  u' встречи с курьером')

        try:
            delivery_type = int(self.cleaned_data.get('delivery_type'))
            self.cleaned_data['delivery_type_label'] = DELIVERY_TYPES[delivery_type]['label']
        except (ValueError, TypeError, KeyError):
            raise ValidationError(u'Выберите тип доставки')

        # бесплатная доставка по Москве только для заказа больше FREE_DELIVERY_PRICE
        if delivery_type == 4 and self.basket_summary < FREE_DELIVERY_PRICE:
            raise ValidationError(u'Бесплатная доставка доступна только для заказа выше %s руб.' % FREE_DELIVERY_PRICE)

        self.delivery_today = self.cleaned_data.get('delivery_date') and \
                              self.cleaned_data.get('delivery_date') == datetime.today().date()

        # Доставка день в день доступна только при выборе сегодняшней даты
        # if delivery_type == 7:
        #     if not self.delivery_today:
        #         raise ValidationError(u'Доставка день в день доступна, если доставка осуществляется сегодня')

        time_key = 'delivery_time_%s' % delivery_type

        try:
            self.cleaned_data['delivery_time'] = DELIVERY_TYPES[delivery_type]['times'][int(self.data[time_key])]
        except (ValueError, TypeError, KeyError, IndexError):
            raise ValidationError(u'Выберите время доставки')

        if 'prices' in DELIVERY_TYPES[delivery_type]:
            price_key = 'delivery_price_%s' % delivery_type

            try:
                price_info = DELIVERY_TYPES[delivery_type]['prices'][int(self.data[price_key])]
            except (ValueError, TypeError, KeyError, IndexError):
                raise ValidationError(u'Укажите вариант с ценой доставки')

            self.cleaned_data['delivery_price'] = price_info['price']
            self.cleaned_data['delivery_type_label'] += ' (%s)' % price_info['label']
        else:
            self.cleaned_data['delivery_price'] = DELIVERY_TYPES[delivery_type]['price']

        return self.cleaned_data
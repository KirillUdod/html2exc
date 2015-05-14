#coding:utf8
from collections import OrderedDict
from decimal import Decimal
from uuid import uuid4

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.mail import send_mail
from django.db import models
from django.db.models.aggregates import Sum
from django.db.transaction import commit_on_success
from django.template.loader import render_to_string
from products.const import BOUQUET_PRICE_TYPE_CHOICES

from walletone.signals import payment_received
from walletone.models import PaymentNotification
from order.const import ORDER_MINIMAL_PRICE, DELIVERY_TYPES, PAY_TYPES
from products.models import BouquetPrice

ORDER_PAY_CASH = 1
ORDER_PAY_ONLINE = 2

ORDER_PAY_TYPES = OrderedDict()
ORDER_PAY_TYPES[ORDER_PAY_CASH] = u'Оплатить наличными курьеру'
ORDER_PAY_TYPES[ORDER_PAY_ONLINE] = u'Оплатить онлайн'

ORDER_CLARIFY_PHONE = 1
ORDER_CLARIFY_NO_PHONE = 2

ORDER_CLARIFY_TYPES = OrderedDict()
ORDER_CLARIFY_TYPES[ORDER_CLARIFY_PHONE] = u'Позвонить получателю для уточнения времени и адреса'
ORDER_CLARIFY_TYPES[ORDER_CLARIFY_NO_PHONE] = u'Везти без звонка в указанный промежуток времени'


class BasketError(Exception):
    pass


class OrderError(Exception):
    pass


class Basket(models.Model):
    session_key = models.CharField(max_length=32, verbose_name=u'session_id', editable=False)
    order = models.ForeignKey('Order', null=True, blank=True, editable=False, related_name='basket')
    quantity = models.PositiveIntegerField(verbose_name=u'Количество')

    product_price = models.ForeignKey(BouquetPrice, verbose_name=u'Цена букета', null=True, blank=True, default=None)
    product_price_type = models.CharField(verbose_name=u'Тип букета', null=True, blank=True, max_length=10,
                                          choices=BOUQUET_PRICE_TYPE_CHOICES.iteritems())

    product_type = models.ForeignKey(ContentType)
    product_id = models.PositiveIntegerField()
    product = generic.GenericForeignKey('product_type', 'product_id')

    class Meta:
        verbose_name = u'Корзина пользователя'
        verbose_name_plural = u'Корзины пользователей'

    def __unicode__(self):
        return u'Корзина пользователя'

    @classmethod
    def add(cls, session_key, product, quantity=1, product_price_id=None, price_type=None):
        price = None
        height = None
        product_price_type = None
        quantity = 1
        total_price = 0
        product_class = type(product).__name__.lower()

        if product_class not in ('unusual', 'special', 'bouquet'):
            raise ValueError(u'Нельзя добавить в корзину неизвестный тип товара')

        product_content_type = ContentType.objects.get_for_model(type(product))

        # если это букет, то добавляем всегда по отедельности, если нет, то увеличиваем количество
        if product_class == 'bouquet':
            # TODO проверку какие цены доступы вообще
            if product_price_id:
                try:
                    bouquet_price = BouquetPrice.objects.get(id=product_price_id)
                    price = bouquet_price.price
                    quantity = bouquet_price.count
                    total_price = price
                    height = bouquet_price.height
                except BouquetPrice.DoesNotExist:
                    pass
            elif price_type in ('small', 'big', ''):
                if price_type:
                    if getattr(product, 'use_%s_price' % price_type, False):
                        price = getattr(product, '%s_price' % price_type)
                        product_price_type = price_type
                        quantity = 1
                elif product.one_price:
                    price = product.price
                    product_price_type = price_type
            else:
                price = product.get_base_price()
                product_price_type = product.default_price_type

            if not price:
                raise BasketError(u'Нельзя добавить товар в корзину с данной ценой')

            basket_product = cls(
                product_type=product_content_type,
                product_id=product.pk,
                session_key=session_key,
                quantity=quantity,
                product_price_id=product_price_id,
                product_price_type=product_price_type
            )
        else:
            price = product.price

            try:
                basket_product = cls.objects.get(
                    product_type=product_content_type,
                    product_id=product.pk,
                    session_key=session_key,
                    order=None
                )
                # если товар был в корзине, то просто увеличиваем его количество
                basket_product.quantity += quantity
            except cls.DoesNotExist:
                basket_product = cls(
                    product_type=product_content_type,
                    product_id=product.pk,
                    session_key=session_key,
                    quantity=quantity
                )

        basket_product.save()

        return price * quantity if not total_price else total_price, quantity, height, product_price_type

    @classmethod
    def remove(cls, session_key, basket_id):
        try:
            cls.objects.filter(id=int(basket_id), session_key=session_key, order_id=None).delete()
        except (ValueError, TypeError):
            pass

    @classmethod
    def get_session_basket(cls, session_key):
        basket = {
            'basket_items': [],
            'summary': 0,
            'goods_count': 0
        }
        for item in cls.objects.filter(session_key=session_key, order_id=None):
            price = None
            if item.product:
                if type(item.product).__name__.lower() == 'bouquet':
                    if item.product_price_id:
                        try:
                            bouquet_price = BouquetPrice.objects.get(id=item.product_price_id)
                            item.height = bouquet_price.height
                            price = bouquet_price.price
                            item.price = price
                        except BouquetPrice.DoesNotExist:
                            pass
                    elif item.product_price_type is not None:
                        if item.product_price_type:
                            if getattr(item.product, 'use_%s_price' % item.product_price_type, False):
                                price = getattr(item.product, '%s_price' % item.product_price_type)
                        elif item.product.one_price:
                            price = item.product.price
                    else:
                        price = item.product.get_base_price()
                else:
                    price = item.product.price

            if price is None:
                cls.remove(session_key, item.id)
                continue

            if not hasattr(item, 'price'):
                item.price = price * item.quantity

            basket['basket_items'].append(item)
            basket['summary'] += item.price
            basket['goods_count'] += 1

        return basket

    @classmethod
    def get_basket_price(cls, session_key):
        return cls.get_session_basket(session_key)['summary']

    @classmethod
    def connect_with_order(cls, session_key, order):
        """
        Привязывает текущую корзину пользователя к заказу. Все должно происходить в транзакции.
        """
        cls.objects.filter(session_key=session_key, order_id=None).update(order=order)

    @property
    def price_type_short_description(self):
        if self.product.one_price:
            price_type = self.product_price_type
            if price_type:
                price_type += '_'

            return getattr(self.product, '%sshort_description' % price_type)
        else:
            return ''


class Order(models.Model):
    unique_hash = models.CharField(max_length=100, verbose_name=u'Уникальный хеш заказа', editable=False, unique=True)

    order_price = models.PositiveIntegerField(verbose_name=u'Сумма заказа, руб.',
                                              help_text=u'Не включая сумму доставки')

    is_paid = models.BooleanField(default=False, verbose_name=u'Оплачен')

    pay_type_old = models.PositiveSmallIntegerField(
        verbose_name=u'Тип оплаты (старая версия)',
        choices=ORDER_PAY_TYPES.iteritems(),
        default=ORDER_PAY_CASH,
        null=True
    )

    pay_type = models.CharField(verbose_name=u'Тип оплаты', max_length=20, choices=PAY_TYPES.iteritems(), null=True,
                                blank=False)

    clarify_type = models.PositiveSmallIntegerField(
        verbose_name=u'Нужно звонить получателю',
        choices=ORDER_CLARIFY_TYPES.iteritems(),
        default=ORDER_CLARIFY_PHONE
    )

    name = models.CharField(max_length=300, verbose_name=u'Имя')
    email = models.EmailField(verbose_name=u'Email')
    phone = models.CharField(max_length=50, verbose_name=u'Телефон')

    customer_is_destination = models.BooleanField(
        verbose_name=u'Я сам являюсь получателем',
        default=False,
        help_text=u'Если выбран этот параметр, то адрес, имя и телефон получателя можно не указывать'
    )
    phone_only = models.BooleanField(verbose_name=u'Я знаю только номер телефона', default=False)
    anonymous_delivery = models.BooleanField(verbose_name=u'Анонимная доставка', default=False)

    destination_name = models.CharField(max_length=300, verbose_name=u'Имя получателя', null=True, blank=True)
    destination_address = models.CharField(verbose_name=u'Адрес получателя', null=True, blank=False, max_length=500)
    destination_phone = models.CharField(max_length=50, verbose_name=u'Телефон получателя', null=True, blank=True)

    comments = models.TextField(verbose_name=u'Комментарии к заказу', blank=True)

    delivery_time = models.CharField(max_length=200, verbose_name=u'Время доставки')
    delivery_date = models.DateField(verbose_name=u'Дата доставки')
    delivery_price = models.PositiveIntegerField(verbose_name=u'Стоимость доставки, руб.',
                                                 help_text=u'Не входит в сумму заказа')
    delivery_type = models.CharField(max_length=200, verbose_name=u'Тип доставки')

    date = models.DateTimeField(verbose_name=u'Дата и время заказа', auto_now_add=True, editable=False)
    positions = models.TextField(verbose_name=u'Состав')

    make_photo = models.BooleanField(verbose_name=u'Сделать фото доставки (с согласия получателя)', default=False)
    send_sms = models.BooleanField(verbose_name=u'Отправить SMS уведомление о доставке', default=False)

    add_card = models.PositiveIntegerField(verbose_name=u'Бесплатные услуги',
                                           choices=((0, u'Добавить карточку: С днем Рождения'),
                                                    (1, u'Добавить карточку: С Любовью'),
                                                    (2, u'Добавить карточку: Поздравляю')),
                                           null=True, blank=True)

    add_toy = models.BooleanField(verbose_name=u'Добавить мягкую игрушку', default=False)

    pay_for_delivery_date = models.DateField(verbose_name=u'Дата', null=True, blank=True,
                                             help_text=u'Дата выезда курьера за оплатой')
    pay_for_delivery_time = models.SmallIntegerField(verbose_name=u'Время', null=False, default=1,
                                                     choices=((1, '09:00 - 12:00'), (2, '12:00 - 15:00'),
                                                              (3, '15:00 - 18:00'), (4, '18:00 - 21:00')),
                                                     help_text=u'Время выезда курьера за оплатой'
                                                     )
    pay_for_delivery_address = models.CharField(verbose_name=u'Адрес', null=True, blank=True, max_length=300,
                                                help_text=u'Адрес выезда курьера за оплатой')

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'

    def __unicode__(self):
        return u'Заказ %s от %s' % (self.name, self.date.strftime('%d.%m.%Y'))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.unique_hash = self.generate_unique_link()

        super(Order, self).save(*args, **kwargs)

    def make_order(self, session_key):
        if self.id:
            raise OrderError(u'Внутренняя ошибка. Попробуйте позже.')

        with commit_on_success():
            # стоимость доставки не суммируется с сумой заказа
            self.order_price = Basket.get_basket_price(session_key)

            for item in Basket.get_session_basket(session_key)['basket_items']:
                if hasattr(item, 'height') and item.height:
                    self.positions += u'%s, количество - %s шт, высота - %s см\r\n' % (
                        unicode(item.product), item.quantity, item.height)
                elif item.product_price_type:
                    self.positions += u'%s (%s), количество - %s\r\n' % (item.product,
                                                                         item.get_product_price_type_display(),
                                                                         item.quantity)
                else:
                    self.positions += u'%s, количество - %s\r\n' % (unicode(item.product), item.quantity)

            self.save()

            Basket.connect_with_order(session_key, self.id)

    def total_price(self):
        return self.order_price + self.delivery_price

    @classmethod
    def generate_unique_link(cls):
        result = str(uuid4()).replace('-', '')
        while cls.objects.filter(unique_hash=result)[:1].count():
            result = str(uuid4()).replace('-', '')

        return result

    @property
    def is_pay_online(self):
        return self.pay_type not in ('nal', 'nalk')


def payment_receiver(*args, **kwargs):
    try:
        order_id = int(kwargs.get('order_id'))
    except (ValueError, TypeError):
        order_id = None

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    # order_payed_sum = Decimal(0)
    # for payment in PaymentNotification.objects.filter(InvId=order_id):
    #     order_payed_sum += Decimal(payment.OutSum)

    order_payed_sum = PaymentNotification.objects.filter(order_id=order.id).values('order_id').annotate(
        amount_sum=Sum('amount'))[0]['amount_sum']

    if order_payed_sum >= order.total_price():
        order.is_paid = True
        order.save()
        send_mail(
            u'Оплата заказа',
            render_to_string('email/order_payed.html', {'order': order, 'payed_sum': order_payed_sum,
                                                        'domain_name': 'mayflo.ru'}),
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_TO_EMAIL],
            fail_silently=False
        )


payment_received.connect(payment_receiver, dispatch_uid='payment_received')
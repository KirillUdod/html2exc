#coding: utf-8
from django.db import models


class PaymentNotification(models.Model):
    order_id = models.BigIntegerField(u'Внутренний номер заказа', db_index=True)
    merchant_order_id = models.BigIntegerField(u'Номер заказа в платежной системе', db_index=True)
    amount = models.DecimalField(u'Сумма платежа', decimal_places=2, max_digits=8)
    # todo currencies

    created_at = models.DateTimeField(u'Дата и время получения уведомления', auto_now_add=True)

    class Meta:
        verbose_name = u'уведомление об успешном платеже'
        verbose_name_plural = u'уведомления об успешных платежах'

    def __unicode__(self):
        return u'Уведомление об оплате заказа %d: %s (%s)' % (self.order_id, self.amount, self.created_at)
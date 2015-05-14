#coding:utf8
from collections import OrderedDict

FREE_DELIVERY_PRICE = 4000  # сумма заказа для бесплатной доставки
ORDER_MINIMAL_PRICE = 0  # минимальная сумма заказа
ADD_TOY_PRICE = 2000  #

DELIVERY_TYPES = {
    1: {'label': u'Стандартная доставка', 'price': 200, 'times': ['09:00 - 12:00', '15:00 - 18:00', '12:00 - 15:00',
                                                                  '18:00 - 21:00']},
    2: {'label': u'Срочная доставка', 'price': 300, 'times': ['09:00 - 11:00', '15:00 - 17:00', '11:00 - 13:00',
                                                              '17:00 - 19:00', '13:00 - 15:00', '19:00 - 21:00']},

    # 3: {'label': u'Express доставка', 'price': 500,
    #     'times': ['09:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00', '14:00 - 15:00',
    #               '15:00 - 16:00', '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00', '19:00 - 20:00',
    #               '20:00 - 21:00']},
    4: {'label': u'Бесплатная доставка', 'price': 0,
        'times': ['09:00-13:00', '13:00-17:00', '17:00-21:00']},

    5: {'label': u'Стандартная доставка по Московской области',
        'times': ['09:00 - 15:00', '15:00 - 21:00'],
        'prices': [
            {'label': u'0-5км', 'price': 400},
            {'label': u'5-10км', 'price': 470},
            {'label': u'10-15км', 'price': 550},
            {'label': u'15-20км', 'price': 650},
            {'label': u'20-25км', 'price': 790},
            {'label': u'25-30км', 'price': 900},
        ]
    },
    # 6: {
    #     'label': u'Express доставка по Московской области',
    #     'times': ['09:00 - 13:00', '13:00 - 17:00', '17:00 - 21:00'],
    #     'prices': [
    #         {'label': u'0-5км', 'price': 500},
    #         {'label': u'5-10км', 'price': 570},
    #         {'label': u'10-15км', 'price': 650},
    #         {'label': u'15-20км', 'price': 750},
    #         {'label': u'20-25км', 'price': 890},
    #         {'label': u'25-30км', 'price': 1000}
    #     ]
    # },
    # 7: {'label': u'Доставка "день в день" за 1,5 часа', 'price': 500,
    #     'times': [u'Доставить за 1,5 часа (с 9:00 - 21:00)']}
}


PAY_TYPES = OrderedDict()
PAY_TYPES['credit_card'] = u'Пластиковая карта'
PAY_TYPES['web_money'] = u'WebMoney'
PAY_TYPES['yandex_money'] = u'Яндекс Деньги'
#PAY_SYSTEM_TYPES['mobi_money'] = u'Мобильный телефон'
PAY_TYPES['beznal'] = u'Платежные терминалы'
PAY_TYPES['nal'] = u'Выезд курьера за оплатой (+250р.)'
PAY_TYPES['nalk'] = u'Наличными курьеру'
PAY_TYPES['sberbank'] = u'Мобильный Банк'
PAY_TYPES['qiwi'] = u'QIWI'


PAY_TYPES_CUR = {
    'credit_card': 'BANKOCEAN2R',
    'web_money': 'WMRM',
    'yandex_money': 'YandexMerchantOcean2R',
    'beznal': 'Qiwi29OceanR',
    'sberbank': 'AlfaBankOceanR',
    'qiwi': 'Qiwi29OceanR'
}
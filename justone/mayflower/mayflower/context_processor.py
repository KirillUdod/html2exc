#coding:utf8
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import OrderedDict

from django.core.urlresolvers import reverse

from mayflower.forms import BackCallForm
from order.const import FREE_DELIVERY_PRICE
from products.models import Review, Bouquet, Special, Unusual, BouquetCategory, UnusualCategory
from order.models import Basket


def back_call_processor(request):
    if request.method.lower() == 'post' and request.POST.get('back_call'):
        back_call_form = BackCallForm(request.POST)
        back_call_form.is_valid()
    else:
        back_call_form = BackCallForm()

    context = {'back_call_form': back_call_form}
    return context

#
# def buy_menu_processor(request):
#     step = 1
#     if request.path == reverse('delivery'):
#         step = 2
#     elif request.path == reverse('order'):
#         step = 3
#
#     return {'buy_step': step}


def reviews_processor(request):
    return {'reviews': Review.objects.all().order_by('-id')}


def main_menu_processor(request):
    categories = {
        'bouquet': {'name': u'Букеты', 'class': BouquetCategory},
        'unusual': {'name': u'Необычности', 'class': UnusualCategory},
        'special': {'name': u'Акция'}
    }
    context = {'main_menu': OrderedDict()}

    for category in categories.iterkeys():
        context['main_menu'][category] = {'active': False}
        context['main_menu'][category]['path'] = reverse('category_page', args=(category, ))
        context['main_menu'][category]['name'] = categories[category].get('name')

        if request.path.startswith(context['main_menu'][category]['path']):
            context['main_menu'][category]['active'] = True

        subcategories_class = categories[category].get('class')
        if subcategories_class:
            context['main_menu'][category]['subcategories'] = subcategories_class.objects.order_by('sort')

    if request.path == '/':
        context['main_menu']['bouquet']['active'] = True

    return context


def basket_processor(request):
    return {'basket': Basket.get_session_basket(request.session._session_key),
            'free_delivery_price': FREE_DELIVERY_PRICE}


# def promo_slider_processor(request):
#     context = {'promo': []}
#
#     for klass in (Bouquet, Unusual, Special):
#         category_type = klass.__name__.lower()
#         context['promo'] += klass.active_objects().filter(use_in_slider=True).order_by('sort')
#         if category_type == 'bouquet':
#             for product in context['promo_' + category_type]:
#                 if not product.one_price:
#                     slider_price = product.bouquetprice_set.order_by('-count')[:1].get()
#                     product.slider_price = slider_price.price
#                     product.slider_quantity = slider_price.count
#
#     # now = datetime.now()
#     # today_day = int(now.strftime('%w'))
#     # context['countdown_date'] = (now + relativedelta(days=8-(today_day if today_day else 7))).replace(hour=0, second=0, minute=0)
#     return context
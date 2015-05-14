#coding:utf8
from django import template
from django.template import TemplateSyntaxError
from django.template.defaultfilters import pluralize, stringfilter

register = template.Library()


@register.filter
def get_product_price(quantity, product):
    return product.get_price_for_quantity(quantity)


@register.filter
def bouquet_pluralize(product, quantity):
    return u'шт.'


@register.filter(is_safe=False)
def rupluralize(value, arg):
    bits = arg.split(u',')

    if value % 10 == 1 and value % 100 != 11:
        return bits[0]
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return bits[1]
    else:
        return bits[2]


@register.filter
def getvalue(dict_, arg):
    return dict_.get(arg)

@register.filter
def number_separator(digit_val, sep=' '):
    return '{0:,}'.format(digit_val).replace(',', sep)
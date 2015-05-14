#coding:utf8
import csv
from itertools import izip_longest
import json
from math import ceil
from random import shuffle
from time import mktime
from urllib import quote

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q, BooleanField, FieldDoesNotExist
from django import forms
from django.http import Http404, HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django import template
from django.utils.timezone import get_current_timezone, now
from django.views.generic import TemplateView

from order.models import Basket, Order, BasketError, OrderError, ORDER_PAY_ONLINE
from products.const import BOUQUET_PRICE_TYPE_CHOICES
from products.models import Special, Bouquet, Unusual, BouquetCategory, UnusualCategory, BouquetCategoryThrough, \
    BouquetPrice
from order.const import *
from mayflower.context_processor import back_call_processor, basket_processor
from order.forms import OrderForm
from products.templatetags.catalog import bouquet_pluralize, rupluralize, number_separator
from utils import get_pagination
from walletone.forms import WalletonePaymentForm, WalletoneResultForm


def add_to_basket(request):
    if request.method == 'POST' and request.POST.get('product_id') and request.POST.get('category_type'):
        if request.POST['category_type'] == 'bouquet':
            product_class = Bouquet.objects
        elif request.POST['category_type'] == 'unusual':
            product_class = Unusual.objects
        else:
            product_class = Special.objects

        product = product_class.get(id=int(request.POST.get('product_id')))

        # fix for removed session_id cookie
        result = {}
        context = {}

        if hasattr(request, 'session') and not request.session.session_key:
            request.session.save()
            request.session.modified = True

        product_quantity = None
        product_price_id = None

        try:
            product_price_id = int(request.POST.get('product_price_id'))
        except (ValueError, TypeError):
            pass

        try:
            product_quantity = int(request.POST.get('product_quantity'))
        except (ValueError, TypeError):
            pass

        price_type = request.POST.get('price_type')

        try:
            price, product_quantity, product_height, price_type = Basket.add(request.session.session_key, product,
                                                                             product_quantity, product_price_id,
                                                                             price_type)
            context['basket'] = Basket.get_session_basket(request.session.session_key)

            if product.CATEGORY_TYPE == 'bouquet':
                if product.one_price:
                    context['text'] = product.name

                    if price_type:
                        context['text'] += u' %s' % BOUQUET_PRICE_TYPE_CHOICES[price_type]
                else:
                    context['text'] = u'%s<br/>%s %s %s' % (product.name, product_quantity,
                                                            bouquet_pluralize(product, product_quantity),
                                                            '' if not product_height else (u'%s см.' % product_height))
            else:
                context['text'] = product.name

            context['price'] = price
            context['price'] = u'<span>%s</span> %s' % (context['price'],
                                                        rupluralize(context['price'], u'рубль,рубля,рублей'))
            context['product'] = product

            try:
                context['unusual_path'] = reverse(
                    'subcategory_page',
                    args=('unusual', UnusualCategory.objects.only('id').order_by('-id')[:1].get().id))
            except UnusualCategory.DoesNotExist:
                context['unusual_path'] = reverse('category_page', args=('unusual', ))

            result['basket_popup'] = render_to_string('blocks/basket_popup.html', context)
            result['goods_count'] = context['basket']['goods_count']
            result['basket'] = render_to_string('blocks/basket_items.html', context)
            result['summary'] = number_separator(context['basket']['summary'])
        except BasketError as ex:
            result['basket_error'] = ex.message

        return HttpResponse(json.dumps(result))


def home(request):
    context = {'categories': OrderedDict(), 'promo': []}
    context['categories']['bouquet'] = []
    context['categories']['unusual'] = []

    for category_type in [BouquetCategory, UnusualCategory]:
        for category in category_type.objects.filter(show_on_main=True).order_by('sort'):
            if category_type == BouquetCategory:
                product_query = Bouquet.active_objects(categories=category)

                context['categories']['bouquet'].append({
                    'category': category,
                    'products_total': product_query.count(),
                    'products': product_query.order_by('bouquetcategorythrough__sort')[:4]
                })
            else:
                product_query = Unusual.active_objects(categories=category)

                context['categories']['unusual'].append({
                    'category': category,
                    'products_total': product_query.count(),
                    'products': product_query.order_by('unusualcategorythrough__sort')[:4]
                })

    for klass in (Bouquet, Unusual, Special, BouquetCategory, UnusualCategory):
        if hasattr(klass, 'active_objects'):
            klass_objects = klass.active_objects()
        else:
            klass_objects = klass.objects

        context['promo'] += klass_objects.filter(use_in_slider=True).order_by('-id')

    return render(request, 'home.html', context)


def index(request, category_type=None, product_id=0):
    """

    """
    context = {}

    product_id = int(product_id)

    if category_type == 'special':
        product_cls = Special
        add_goods_field = None
    elif category_type == 'bouquet':
        product_cls = Bouquet
        add_goods_field = 'show_in_bouquets'
    elif category_type == 'unusual':
        product_cls = Unusual
        add_goods_field = 'show_in_unusuals'
    else:
        raise Http404()

    try:
        product = product_cls.active_objects().get(id=product_id)
    except product_cls.DoesNotExist:
        raise Http404()

    if category_type != 'special':
        context['add_goods'] = list(Bouquet.active_objects().filter(**{add_goods_field: True}))
        context['add_goods'].extend(list(Unusual.active_objects().filter(**{add_goods_field: True})))
        context['add_goods'].extend(list(Special.active_objects().filter(**{add_goods_field: True})))
        shuffle(context['add_goods'])

    # добавление в корзину
    if request.method == 'POST' and product:
        category_type = request.POST['category_type']
        if category_type == 'bouquet':
            product_class = Bouquet.objects
        elif category_type == 'unusual':
            product_class = Unusual.objects
        else:
            product_class = Special.objects

        try:
            return add_to_basket(request, context, product_class.get(id=int(request.POST.get('product_id'))))
        except (ValueError, TypeError, ObjectDoesNotExist):
            raise Http404()

    if product_cls == Bouquet and product.use_small_or_big_price:
        context['product_prices'] = []

        for price_type, label in (('small', u'Уменьшенный'), ('', u'Стандартный (на фото)'), ('big', u'Увеличенный')):
            if price_type == '' or getattr(product, 'use_%s_price' % price_type, False):
                selected = product.default_price_type == price_type
                if price_type:
                    price_type += '_'

                context['product_prices'].append({
                    'label': label,
                    'old_price': getattr(product, '%sold_price' % price_type),
                    'price': getattr(product, '%sprice' % price_type),
                    'type': price_type[:-1],
                    'description': getattr(product, '%sshort_description' % price_type),
                    'selected': selected
                })

    context['active_product'] = product
    context['active_category_type'] = category_type
    if hasattr(product, 'categories'):
        # если товар относится только к одной категории, то подсвечиваем ее в меню
        categories = product.categories.all().only('id')[:2]
        if len(categories) == 1:
            context['active_category'] = categories[0].id

    context['global_category'] = product._meta.verbose_name_plural

    return render(request, 'index.html', context)


def catalog_category(request, category_type=None, category_id=0, current_page=1):
    context = {}
    items_on_page = 12
    category_id = int(category_id)

    if category_type == 'special':
        product_query = Special
        category = None
    elif category_type == 'bouquet':
        product_query = Bouquet
        try:
            category = BouquetCategory.objects.get(id=category_id)
        except BouquetCategory.DoesNotExist:
            raise Http404()
    elif category_type == 'unusual':
        product_query = Unusual
        try:
            category = UnusualCategory.objects.get(id=category_id)
        except UnusualCategory.DoesNotExist:
            raise Http404()
    else:
        raise Http404()

    product_query = product_query.active_objects()

    if category_type != 'special':
        through_model_prefix = category_type + 'categorythrough__'
        product_query = product_query.filter(**{'%scategory_id' % through_model_prefix: category.id})\
            .order_by('%ssort' % through_model_prefix)

    products_total = product_query.count()

    try:
        current_page = int(current_page)
    except (ValueError, TypeError):
        current_page = 1

    if current_page < 1 or current_page > ceil(products_total / float(items_on_page)):
        raise Http404()

    context['products_total'] = products_total
    context['active_category_type'] = category_type
    context['active_category'] = category_id
    context['category'] = category
    context['current_page'] = current_page
    if 'show_all' in request.GET:
        context['products'] = product_query
        context['show_all'] = True
    else:
        context['products'] = product_query[(current_page - 1) * items_on_page: current_page * items_on_page]
        context['pagination'] = get_pagination(products_total, current_page, items_on_page)

    return render(request, 'subcategory.html', context)


def back_call(request):
    context = back_call_processor(request)
    if context['back_call_form'].is_valid():
        email_context = {
            'name': context['back_call_form'].cleaned_data.get('name'),
            'phone': context['back_call_form'].cleaned_data.get('phone')
        }
        send_mail(
            u'Новая заявка на обратный звонок',
            render_to_string('email/back_call.html', email_context),
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_TO_EMAIL],
            fail_silently=True
        )

        context['back_call_message'] = u'Заявка отправлена'
    return render(request, 'forms/form_output.html', context)


def send_order_email(order, domain_name):
    context = {
        'order': order,
        'domain_name': domain_name,
        'order_info': OrderedDict()
    }
    fields = ['date', 'name', 'email', 'phone', 'destination_address',  'phone_only', 'customer_is_destination',
              'clarify_type', 'anonymous_delivery', 'make_photo', 'send_sms', 'add_card', 'add_toy']

    if not order.customer_is_destination:
        fields.extend(['destination_name', 'destination_phone'])

    fields.extend(['delivery_time', 'delivery_date', 'delivery_type', 'delivery_price', 'pay_type'])

    if order.pay_type == 'nal':
        fields.extend(['pay_for_delivery_date', 'pay_for_delivery_time', 'pay_for_delivery_address'])

    fields.extend(['order_price', 'comments', 'positions'])

    for field_name in fields:
        try:
            field = Order._meta.get_field(field_name)
        except FieldDoesNotExist:
            continue

        field_label = field.verbose_name

        if field.choices:
            field_value = getattr(order, 'get_%s_display' % field_name)
        elif isinstance(field, BooleanField):
            field_value = u'Да' if getattr(order, field_name) else u'Нет'
        else:
            field_value = getattr(order, field_name)

        if field_name in ('pay_for_delivery_date', 'pay_for_delivery_time', 'pay_for_delivery_address'):
            field_label += u' выезда курьера за оплатой'

        if field_name == 'date':
            timezone = get_current_timezone()
            field_value = field_value.astimezone(timezone)
            if hasattr(timezone, 'normalize'):
                field_value = timezone.normalize(field_value)

            field_value = field_value.strftime('%d-%m-%Y %H:%M')

        if not field_value:
            field_value = '-'

        context['order_info'][field_name] = field_label, field_value

    context['order_info']['full_order_price'] = u'Полная сумма заказа', u'%s руб.' % order.total_price()

    send_mail(
        u'Новый заказ',
        render_to_string('email/new_order_admin.html', context),
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_TO_EMAIL],
        fail_silently=True
    )

    order_link = 'http://%s%s' % (domain_name, reverse('order_show', args=(order.unique_hash, )))
    context['order_info']['link'] = u'Ваша ссылка на заказ', order_link

    del context['order_info']['phone_only']
    del context['order_info']['customer_is_destination']

    send_mail(
        u'Заказ на сайте %s' % domain_name,
        render_to_string('email/new_order.html', context),
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=True
    )


def order(request):
    context = {}

    basket = Basket.get_session_basket(request.session._session_key)

    # if not basket['goods_count']:
    #     return HttpResponseRedirect('/')

    if request.method.lower() == 'post':
        order_form = OrderForm(request.POST, basket_summary=basket['summary'])
        context['show_form'] = True

        if order_form.is_valid():
            order_instance = order_form.save(commit=False)
            order_instance.delivery_price = order_form.cleaned_data['delivery_price']
            order_instance.delivery_type = order_form.cleaned_data['delivery_type_label']
            order_instance.delivery_time = order_form.cleaned_data['delivery_time']
            order_instance.make_order(request.session.session_key)

            send_order_email(order_instance, request.META.get('HTTP_HOST'))

            if order_instance.pay_type not in ('nal', 'nalk'):
                # оплата онлайн
                payment_url = WalletonePaymentForm(initial={
                    'WMI_PAYMENT_AMOUNT': order_instance.total_price(),
                    'WMI_PAYMENT_NO': order_instance.id,
                    'WMI_DESCRIPTION': u'%s заказ №%s' % (request.get_host(), order_instance.id)
                }, host=settings.HOST).get_redirect_url()
                return HttpResponseRedirect(payment_url)
            else:
                # оплата наличными
                return HttpResponseRedirect(reverse('ordered', args=(order_instance.id, )))

    else:
        order_form = OrderForm(basket_summary=basket['summary'])

    context['for_order'] = True
    context['order_form'] = order_form
    context['delivery_types'] = DELIVERY_TYPES
    context['pay_types'] = PAY_TYPES
    context['free_delivery_price'] = FREE_DELIVERY_PRICE
    context['add_toy_price'] = ADD_TOY_PRICE

    add_goods_filter = Q(show_in_bouquets=True)
    context['add_goods'] = list(Bouquet.active_objects().filter(add_goods_filter))
    context['add_goods'].extend(list(Unusual.active_objects().filter(add_goods_filter)))
    context['add_goods'].extend(list(Special.active_objects().filter(add_goods_filter)))
    shuffle(context['add_goods'])

    return render(request, 'order.html', context)


def ordered(request, order_id):
    try:
        order_instance = Order.objects.filter(id=order_id, basket__session_key=request.session._session_key)[:1].get()
    except Order.DoesNotExist:
        raise Http404()

    context = {
        'order': order_instance
    }

    if order_instance.is_pay_online and not order_instance.is_paid:
        init = {
            'WMI_PAYMENT_AMOUNT': order_instance.total_price(),
            'WMI_PAYMENT_NO': order_instance.id,
            'WMI_DESCRIPTION': u'%s заказ №%s' % (request.get_host(), order_instance.id)
        }

        context['pay_online'] = True
        context['pay_href'] = WalletonePaymentForm(initial=init, host=settings.HOST).get_redirect_url()

    return render(request, 'ordered.html', context)


def order_show(request, order_hash):
    try:
        order_instance = Order.objects.get(unique_hash=order_hash)
    except Order.DoesNotExist:
        raise Http404()

    context = {'order': order_instance}

    if order_instance.is_pay_online:
        init = {
            'WMI_PAYMENT_AMOUNT': order_instance.total_price(),
            'WMI_PAYMENT_NO': order_instance.id,
            'WMI_DESCRIPTION': u'%s заказ №%s' % (request.get_host(), order_instance.id)
        }

        context['pay_online'] = True
        context['pay_href'] = WalletonePaymentForm(initial=init, host=settings.HOST).get_redirect_url()

    return render(request, 'order_show.html', context)


def remove_from_basket(request):
    if request.is_ajax() and 'remove_basket_product' in request.POST:
        # fix for removed session_id cookie
        if hasattr(request, 'session') and not request.session.session_key:
            request.session.save()
            request.session.modified = True

        Basket.remove(request.session._session_key, request.POST.get('remove_basket_product'))
        basket = Basket.get_session_basket(request.session._session_key)

        return HttpResponse(json.dumps({
            'basket': render_to_string('blocks/basket_items.html', basket_processor(request)),
            'goods_count': basket['goods_count'],
            'summary': number_separator(basket['summary'])
        }))
    else:
        return Http404()


def page(request, code):
    template_name = 'pages/%s.html' % code
    try:
        template.loader.get_template(template_name)
        return render(
            request,
            template_name,
            {'delivery_types': DELIVERY_TYPES}
        )
    except template.TemplateDoesNotExist:
        raise Http404()


class PricesUpdateDownloadForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=BouquetCategory.objects.all(), label=u'Выберите категорию')
    active_only = forms.BooleanField(label=u'Только активные', initial=False, required=False)


class PricesUpdateUploadForm(forms.Form):
    csv_file = forms.FileField(label=u'Выберите файл')


def stream_file_response(file_name, stream):
    response = StreamingHttpResponse(stream)
    response['Content-Type'] = 'application/octet'
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % quote(file_name)
    response['Content-Description'] = 'File Transfer'
    response['Content-Transfer-Encoding'] = 'binary'
    response['Expires'] = '0'
    response['Cache-Control'] = 'must-revalidate'
    response['Pragma'] = 'public'
    return response


class PricesUpdateView(TemplateView):
    template_name = 'admin/prices_update.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['download_form'] = PricesUpdateDownloadForm()
        context['upload_form'] = PricesUpdateUploadForm()

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['download_form'] = PricesUpdateDownloadForm()
        context['upload_form'] = PricesUpdateUploadForm()

        if request.POST['action'] == 'download':
            download_form = PricesUpdateDownloadForm(request.POST)

            if download_form.is_valid():
                response = HttpResponse()
                response['Content-Type'] = 'application/octet'
                response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % quote(u'mayflo_prices_%s.csv' % now().strftime('%d.%m.%Y'))
                response['Content-Description'] = 'File Transfer'
                response['Content-Transfer-Encoding'] = 'binary'
                response['Expires'] = '0'
                response['Cache-Control'] = 'must-revalidate'
                response['Pragma'] = 'public'

                writer = csv.writer(response, dialect='excel', quoting=csv.QUOTE_MINIMAL, delimiter=';')
                writer.writerows(self.generate_csv_rows(**download_form.cleaned_data))
                return response

            context['download_form'] = download_form
        elif request.POST['action'] == 'upload':
            upload_form = PricesUpdateUploadForm(request.POST, files=request.FILES)

            if upload_form.is_valid():
                context['product_processed'], context['errors'] = self.update_prices(**upload_form.cleaned_data)

            context['upload_form'] = upload_form

        return self.render_to_response(context)

    BASE_HEADER = [u'Номер ID', u'Название', u'Размер', u'Кол-во', u'Цена']
    BASE_HEADER_CODES = ['id', 'name', 'size', 'quantity', 'price']
    NUMBER_FORMAT = '%s!'
    EMPTY = '-'

    def generate_csv_rows(self, categories, active_only):
        header = self.BASE_HEADER[:]

        header.extend(u'%s (id:%s)' % (category.name, category.id) for category in categories)

        yield map(lambda val: val.encode('cp1251'), header)

        query_filter = {
            'categories__in': categories,
        }

        if active_only:
            query_filter['active'] = True

        for product in Bouquet.objects.filter(**query_filter).order_by('id'):
            category_row = []

            product_categories = dict(BouquetCategoryThrough.objects.filter(product=product).values_list('category_id', 'sort'))

            for category in categories:
                if category.id in product_categories:
                    category_row.append(self.NUMBER_FORMAT % product_categories[category.id])
                else:
                    category_row.append(self.EMPTY)

            base_row = [product.id, product.name.encode('cp1251')]

            if not product.one_price:
                for height, height_prices in product._get_prices()[0].iteritems():
                    for quantity, price_info in height_prices.iteritems():
                        row = base_row[:]
                        row.append((self.NUMBER_FORMAT % height) if height else self.EMPTY)
                        row.append(self.NUMBER_FORMAT % quantity)
                        row.append(self.NUMBER_FORMAT % price_info['price'])
                        row.extend(category_row)

                        yield row
            else:
                for price_type, price_title in Bouquet.PRICE_TYPES.iteritems():
                    if getattr(product, 'use_%s_price' % price_type):
                        row = base_row[:]
                        row.append(price_title.encode('cp1251'))
                        row.append(self.EMPTY)

                        row.append(self.NUMBER_FORMAT % getattr(product, '%s_price' % price_type))

                        row.extend(category_row)

                        yield row

    def read_header(self, header):
        categories = []

        for csv_col_name, base_col_name in izip_longest(header, self.BASE_HEADER_CODES):
            if not base_col_name:
                categories.append(int(csv_col_name.split('id:', 1)[-1].strip(')')))

        return categories

    @staticmethod
    def _int(val):
        return int(val.strip('!'))

    def update_prices(self, csv_file):
        reader = csv.reader(csv_file, quoting=csv.QUOTE_MINIMAL, delimiter=';')
        cols_codes = self.BASE_HEADER_CODES[:]
        categories_ids = []
        total_cols_cnt = len(cols_codes)
        imported_rows = -1
        errors = []
        reverse_price_types = {title.lower(): code for code, title in Bouquet.PRICE_TYPES.iteritems()}

        for row in reader:
            imported_rows += 1
	    
	    print row

            if not imported_rows:
                try:
                    categories_ids = self.read_header(row)
                except (ValueError, TypeError):
                    errors.append(u'Неверные ID категорий в заголовке')
                    break

                total_cols_cnt += len(categories_ids)
            else:
                if total_cols_cnt != len(row):
                    errors.append(u'Неверный формат строки в csv файле: %s' % ' '.join(row))
                    continue

                product_info = dict(zip(cols_codes, map(lambda val: (val or self.EMPTY).decode('cp1251'), row[:len(cols_codes)])))
                product_info['categories'] = dict(zip(categories_ids, map(lambda val: (val or self.EMPTY), row[len(cols_codes):])))
	    
		# print product_info

                try:
                    product = Bouquet.objects.get(id=product_info['id'])
                except Bouquet.DoesNotExist:
                    errors.append(u'Товар с ID %s не найден в базе' % product_info['id'])
                    continue

                price_type_title = product_info['size'].lower()

                if price_type_title in reverse_price_types:
                    try:
                        new_price = self._int(product_info['price'])
                    except (ValueError, TypeError):
                        errors.append(u'Для товара с ID %s неверено указана цена для размера %s: %s' %
                                      (product_info['id'], product_info['size'], product_info['price']))
                        continue

                    price_type = reverse_price_types[price_type_title]

                    if getattr(product, '%s_price' % price_type) != new_price:
                        setattr(product, '%s_price' % price_type, new_price)
                        product.save()
                else:
                    try:
                        height = None if product_info['size'] == self.EMPTY else self._int(product_info['size'])
                    except (ValueError, TypeError):
                        errors.append(u'Для товара с ID %s неверено указан размер: %s' % (product_info['id'],
                                                                                          product_info['size']))
                        continue

                    try:
                        quantity = self._int(product_info['quantity'])
                    except (ValueError, TypeError):
                        errors.append(u'Для товара с ID %s неверено указано количество для размера %s: %s' %
                                      (product_info['id'], product_info['size'], product_info['quantity']))
                        continue

                    try:
                        price = self._int(product_info['price'])
                    except (ValueError, TypeError):
                        errors.append(u'Для товара с ID %s неверено указана цена для размера %s и количества %s: %s' %
                                      (product_info['id'], product_info['size'], product_info['quantity'],
                                       product_info['price']))
                        continue

                    try:
                        bouquet_price = BouquetPrice.objects.get(product=product, height=height, count=quantity)
                        created = False
                    except BouquetPrice.DoesNotExist:
                        bouquet_price = BouquetPrice(product=product, height=height, count=quantity)
                        created = True

                    if created or bouquet_price.price != price:
                        bouquet_price.price = price
                        bouquet_price.save()

                delete_from_categories = []

                for category_id, category_sort in product_info['categories'].iteritems():
                    if category_sort == self.EMPTY:
                        delete_from_categories.append(category_id)
                    else:
                        try:
                            category_sort = self._int(category_sort)
                        except (ValueError, TypeError):
                            errors.append(u'Для товара с ID %s задан неверный формат сортировки для категории'
                                          u' c ID %s: %s' % (product.id, category_id, category_sort))
                            continue

                        bouquet_category, created = BouquetCategoryThrough.objects.get_or_create(product=product,
                                                                                                 category_id=category_id)
                        if created or bouquet_category.sort != category_sort:
                            bouquet_category.sort = category_sort
                            bouquet_category.save()

                if delete_from_categories:
                    if BouquetCategoryThrough.objects.filter(product=product, category_id__in=delete_from_categories).exists():
                        BouquetCategoryThrough.objects.filter(product=product, category_id__in=delete_from_categories).delete()

        return imported_rows, errors
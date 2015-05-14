#coding:utf8
from django.contrib.admin import site
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from products.forms import BouquetAdminForm
from products.models import Bouquet, BouquetCategory, UnusualCategory, Unusual, Special, Review, \
    BouquetCategoryThrough, UnusualCategoryThrough, BouquetPrice


class BouquetCategoryInline(admin.TabularInline):
    model = BouquetCategoryThrough


class BouquetPriceInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_price = False
        price_with_null_height = False
        prices_without_null_height = False
        has_prices = False

        for form in self.forms:
            if not form.is_valid():
                return

            if form.cleaned_data and not form.cleaned_data.get('DELETED'):
                price = form.cleaned_data
                has_prices = True

                if price['main']:
                    if not main_price:
                        main_price = True
                    else:
                        raise ValidationError(u'Нельзя указывать две основных цены')

                if not price['height']:
                    price_with_null_height = True
                else:
                    prices_without_null_height = True

        if not has_prices and not (self.instance.one_price and self.instance.price):
            raise ValidationError(u'Вы не указали ни одной цены')

        if price_with_null_height and prices_without_null_height:
            raise ValidationError(u'Нельзя одновременно указывать цены с высотой и без высоты')

        if not main_price and has_prices:
            raise ValidationError(u'Укажите основную цену')


class BouquetPriceInline(admin.TabularInline):
    model = BouquetPrice
    ordering = ['height', 'count']
    formset = BouquetPriceInlineFormset

    def has_add_permission(self, request):
        return True


class UnusualCategoryInline(admin.TabularInline):
    model = UnusualCategoryThrough


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['categories', 'active']


class BaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_absolute_url']


class BouquetAdmin(ProductAdmin):
    inlines = [BouquetCategoryInline, BouquetPriceInline]
    form = BouquetAdminForm
    change_list_template = 'admin/bouquet/change_list_template.html'


class UnusualAdmin(ProductAdmin):
    inlines = [UnusualCategoryInline]


site.register(Bouquet, BouquetAdmin)
site.register(BouquetCategory, BaseAdmin)

site.register(Unusual, UnusualAdmin)
site.register(UnusualCategory, BaseAdmin)

site.register(Special, BaseAdmin)

site.register(Review)
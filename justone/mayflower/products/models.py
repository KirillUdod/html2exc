#coding:utf8
from collections import OrderedDict
import os
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from PIL import Image
from products.const import BOUQUET_PRICE_TYPE_CHOICES


def resize_picture(image_path, width, height, max_width, max_height, ):
    if (max_width and width > max_width) or (max_height and height > max_height):
        img = Image.open(image_path)
        img.thumbnail((max_width if max_width else width, max_height if max_height else height), Image.ANTIALIAS)
        img.save(image_path)


class BaseProduct(models.Model):
    name = models.CharField(max_length=500, verbose_name=u'Название')
    active = models.BooleanField(default=True, verbose_name=u'Активность')

    picture = models.ImageField(
        upload_to='products_pictures',
        verbose_name=u'Большая картинка'
    )

    category_picture = models.ImageField(
        upload_to='categories_pictures',
        verbose_name=u'Картинка для списка товаров в категории',
        help_text=u'Будет пропорционально уменьшена (макс. ширина - 165px, макс. высота - 195px)',
        null=True,  # для обратной совместимости
        blank=False
    )

    description = models.TextField(verbose_name=u'Подробное описание товара')
    short_description = models.CharField(max_length=100, verbose_name=u'Короткое описание товара', blank=True)

    use_in_slider = models.BooleanField(verbose_name=u'Использовать в промо слайдере', default=False)
    slider_photo = models.ImageField(
        upload_to='products_slider',
        verbose_name=u'Картинка для слайдера',
        null=True,
        blank=True
    )
    show_in_bouquets = models.BooleanField(verbose_name=u'Отображать в дополнительных товарах в Букетах',
                                           default=False)
    show_in_unusuals = models.BooleanField(verbose_name=u'Отображать в дополнительных товарах в Необычностях',
                                           default=False)

    picture_max_width = 585
    picture_max_height = None

    slider_photo_max_width = 940
    slider_photo_max_height = 330

    category_picture_max_width = 165
    category_picture_max_height = 195

    class Meta:
        abstract = True
        ordering = ('id', )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        db_instance = None

        if self.pk:
            try:
                db_instance = self.__class__.objects.get(pk = self.id)
            except self.DoesNotExist:
                pass

        super(BaseProduct, self).save(*args, **kwargs)

        for field_name in ('picture', 'slider_photo', 'category_picture'):
            db_field_value = getattr(db_instance, field_name, None)
            field_value = getattr(self, field_name, None)

            if db_instance and db_field_value and db_field_value != field_value:
                db_field_value.delete(False)

            if field_value and os.path.exists(field_value.path):
                resize_picture(
                    field_value.path,
                    field_value.width,
                    field_value.height,
                    getattr(self, field_name + '_max_width', None),
                    getattr(self, field_name + '_max_height', None)
                )

    def delete(self, using=None):
        super(BaseProduct, self).delete()

        for field_name in ('picture', 'slider_photo', 'category_picture'):
            try:
                field = getattr(self, field_name)
                if field:
                    field.delete(False)
            except:
                pass

    def get_absolute_url(self):
        return reverse('product_page',
            kwargs={'category_type': self.CATEGORY_TYPE, 'product_id': self.id})

    @classmethod
    def active_objects(cls, **kwargs):
        return cls.objects.filter(active=True, **kwargs)

    def clean(self):
        if self.use_in_slider and not self.slider_photo:
            raise ValidationError(u'Вы указали, что фото должно отображаться в слайдере, '
                                  u'но не указали фото для слайдера')

    def get_base_price(self):
        return self.price


class BaseCategory(models.Model):
    name = models.CharField(max_length=500, verbose_name=u'Название')
    sort = models.PositiveIntegerField(default=100, verbose_name=u'Сортировка')
    show_on_main = models.BooleanField(verbose_name=u'Показывать на главной', default=False)
    picture = models.ImageField(
        upload_to='categories_pictures',
        verbose_name=u'Картинка'
    )

    use_in_slider = models.BooleanField(verbose_name=u'Использовать в промо слайдере', default=False)
    slider_photo = models.ImageField(
        upload_to='products_slider',
        verbose_name=u'Картинка для слайдера',
        null=True,
        blank=True
    )

    picture_max_width = 43
    picture_max_height = 43

    slider_photo_max_width = 940
    slider_photo_max_height = 330

    CATEGORY_TYPE = None

    class Meta:
        abstract = True
        ordering = ('id', )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subcategory_page', args=(self.CATEGORY_TYPE, self.id))

    get_absolute_url.short_description = u'Ссылка'

    def save(self, *args, **kwargs):
        db_instance = None

        if self.pk:
            try:
                db_instance = self.__class__.objects.get(pk = self.id)
            except self.DoesNotExist:
                pass

        super(BaseCategory, self).save(*args, **kwargs)

        for field_name in ('picture', 'slider_photo', 'category_picture'):
            db_field_value = getattr(db_instance, field_name, None)
            field_value = getattr(self, field_name, None)

            if db_instance and db_field_value and db_field_value != field_value:
                db_field_value.delete(False)

            if field_value and os.path.exists(field_value.path):
                resize_picture(
                    field_value.path,
                    field_value.width,
                    field_value.height,
                    getattr(self, field_name + '_max_width', None),
                    getattr(self, field_name + '_max_height', None)
                )

    def delete(self, using=None):
        super(BaseCategory, self).delete()
        try:
            self.picture.delete(False)
            self.slider_photo.delete(False)
        except:
            pass

    def clean(self):
        if self.use_in_slider and not self.slider_photo:
            raise ValidationError(u'Вы указали, что фото должно отображаться в слайдере, '
                                  u'но не указали фото для слайдера')


class Product(BaseProduct):
    price = models.PositiveIntegerField(verbose_name=u'Цена единцы товара, руб.')
    old_price = models.PositiveIntegerField(verbose_name=u'Старая цена единицы товара, руб.', blank=True, null=True)

    class Meta:
        abstract = True


class BouquetCategory(BaseCategory):
    CATEGORY_TYPE = 'bouquet'

    class Meta:
        verbose_name = u'Категория букетов'
        verbose_name_plural = u'Категории букетов'


class BouquetCategoryThrough(models.Model):
    category = models.ForeignKey('BouquetCategory', verbose_name=u'Категория')
    product = models.ForeignKey('Bouquet', verbose_name=u'Букет')
    sort = models.PositiveIntegerField(default=100, verbose_name=u'Сортировка')

    class Meta:
        verbose_name = u'Категория букета'
        verbose_name_plural = u'Категории букета'

    def __unicode__(self):
        return u''


class BouquetPrice(models.Model):
    product = models.ForeignKey('Bouquet', verbose_name=u'Букет')

    height = models.PositiveIntegerField(verbose_name=u'Высота букета', help_text=u'в санитметрах',
                                         null=True, default=None, blank=True)
    count = models.PositiveIntegerField(verbose_name=u'Количество')
    price = models.PositiveIntegerField(verbose_name=u'Цена')
    old_price = models.PositiveIntegerField(verbose_name=u'Старая цена', blank=True, default=None, null=True)
    main = models.BooleanField(verbose_name=u'Основная цена', default=False)

    class Meta:
        verbose_name = u'цена'
        verbose_name_plural = u'цены'
        unique_together = ('product', 'height', 'count')

    def __unicode__(self):
        return u''

    def clean(self):
        filter_query = type(self).objects.filter(
            **{field: getattr(self, field) for field in self._meta.unique_together[0]})

        if self.pk:
            filter_query = filter_query.exclude(pk=self.pk)

        if filter_query.exists():
            raise ValidationError(u'Цена для этого букета с такой высотой и количеством уже задана')


class Bouquet(BaseProduct):
    categories = models.ManyToManyField(BouquetCategory, through=BouquetCategoryThrough, verbose_name=u'Категории')

    one_price = models.BooleanField(verbose_name=u'Используется только одна цена', default=False)
    price = models.PositiveIntegerField(verbose_name=u'Цена, руб.', blank=True, null=True)
    old_price = models.PositiveIntegerField(verbose_name=u'Старая цена, руб.', blank=True, null=True)

    use_small_price = models.BooleanField(verbose_name=u'Уменьшенный букет', default=False)
    small_price = models.PositiveIntegerField(verbose_name=u'Цена уменьшенного букета, руб.', blank=True, null=True,
                                              help_text=u'Обязательно для ввода, если отмечена галочка '
                                                        u'"Уменьшенный букет"')
    small_old_price = models.PositiveIntegerField(verbose_name=u'Старая цена уменьшенного букета, руб.', blank=True,
                                                  null=True)
    small_short_description = models.TextField(verbose_name=u'Описание для уменьшенного букета', blank=True,
                                               help_text=u'Обязательно для ввода, если отмечена галочка '
                                                         u'"Уменьшенный букет"')

    use_big_price = models.BooleanField(verbose_name=u'Увеличенный букет', default=False)
    big_price = models.PositiveIntegerField(verbose_name=u'Цена увеличенного букета, руб.', blank=True, null=True,
                                            help_text=u'Обязательно для ввода, если отмечена галочка '
                                                      u'"Уменьшенный букет"')
    big_old_price = models.PositiveIntegerField(verbose_name=u'Старая цена увеличенного букета, руб.', blank=True,
                                                null=True)
    big_short_description = models.TextField(verbose_name=u'Описание для увеличенного букета', blank=True,
                                             help_text=u'Обязательно для ввода, если отмечена галочка '
                                                       u'"Уменьшенный букет"')

    default_price_type = models.CharField(verbose_name=u'Букет (цена) по умолчанию', default='', blank=True,
                                          choices=BOUQUET_PRICE_TYPE_CHOICES.iteritems(), max_length=10,
                                          help_text=u'По умолчанию используется стандартная цена')

    CATEGORY_TYPE = 'bouquet'

    PRICE_TYPES = OrderedDict((('small', u'Маленький'), ('base', u'Стандартный'), ('big', u'Большой')))

    dependencies = {
        ('use_small_price', True): ['small_price', 'small_short_description'],
        ('use_big_price', True): ['big_price', 'big_short_description'],
        ('one_price', True): ['price']
    }

    class Meta:
        verbose_name = u'Букет'
        verbose_name_plural = u'Букеты'

    @property
    def use_base_price(self):
        return self.one_price

    def _get_base_price(self):
        return self.price

    def _set_base_price(self, value):
        self.price = value

    base_price = property(_get_base_price, _set_base_price)

    def clean(self):
        if self.one_price and self.default_price_type:
            if not getattr(self, 'use_%s_price' % self.default_price_type)\
                    or not getattr(self, '%s_price', self.default_price_type):
                raise ValidationError(u'Выбран "%s" букет по умолчанию, но не указана его цена или не указано, что он'
                                      u' доступен для выбора' % self.get_default_price_type_display())
        # if self.one_price and not self.price:
        #     raise ValidationError(u'Вы указали использовать только одну цену, но не указали ее')

    def _get_prices(self):
        """
        Возвращает OrderedDict, где ключ - это высота, а значение OrderedDict, где ключ - это количество, а значение -
        словарь, id - это id цены с данной высотой и количеством, а price - сама цена.
        """
        prices = OrderedDict()
        main_price = None

        for price in self.bouquetprice_set.order_by('height', 'count'):
            tmp = prices.setdefault(price.height, OrderedDict())
            tmp[price.count] = {'id': price.pk, 'price': price.price}
            if price.old_price:
                tmp[price.count]['old_price'] = price.old_price

            if price.main:
                main_price = price

        return prices, main_price

    @property
    def prices_info(self):
        if not hasattr(self, '_prices_info'):
            setattr(self, '_prices_info', self._get_prices())

        return getattr(self, '_prices_info')[0]

    @property
    def main_price(self):
        if not hasattr(self, '_prices_info'):
            setattr(self, '_prices_info', self._get_prices())

        return getattr(self, '_prices_info')[1]

    def get_base_price(self):
        if not self.one_price:
            return self.main_price.price
        else:
            price_type = self.default_price_type
            if price_type:
                price_type += '_'

            return getattr(self, '%sprice' % price_type)

    @property
    def use_small_or_big_price(self):
        return self.use_big_price or self.use_small_price


class UnusualCategory(BaseCategory):
    CATEGORY_TYPE = 'unusual'

    class Meta:
        verbose_name = u'Категория необычностей'
        verbose_name_plural = u'Категории необычностей'


class UnusualCategoryThrough(models.Model):
    category = models.ForeignKey('UnusualCategory', verbose_name=u'Категория')
    product = models.ForeignKey('Unusual', verbose_name=u'Необычность')
    sort = models.PositiveIntegerField(default=100, verbose_name=u'Сортировка')

    class Meta:
        verbose_name = u'Категория необычности'
        verbose_name_plural = u'Категории необычности'

    def __unicode__(self):
        return u''


class Unusual(Product):
    categories = models.ManyToManyField(UnusualCategory, through=UnusualCategoryThrough, verbose_name=u'Категории')

    CATEGORY_TYPE = 'unusual'

    class Meta:
        verbose_name = u'Необычность'
        verbose_name_plural = u'Необычности'


class Special(Product):
    sort = models.PositiveIntegerField(default=100, verbose_name=u'Сортировка')

    CATEGORY_TYPE = 'special'

    class Meta:
        verbose_name = u'Спецпредложение'
        verbose_name_plural = u'Спецпредложения'


class Review(models.Model):
    name = models.CharField(verbose_name=u'Имя', max_length=50)
    text = models.TextField(verbose_name=u'Текст отзыва')
    age = models.CharField(verbose_name=u'Возраст', max_length=30, help_text=u'Например, 20 лет')
    picture = models.ImageField(verbose_name=u'Фото', null=True, blank=True, upload_to='reviews')

    picture_max_width = 60
    picture_max_height = 60

    class Meta:
        verbose_name = u'отзыв'
        verbose_name_plural = u'отзывы'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        dbInstance = None

        if self.pk:
            try:
                dbInstance = self.__class__.objects.get(pk = self.id)
            except self.DoesNotExist:
                pass

        super(Review, self).save(*args, **kwargs)

        if dbInstance and dbInstance.picture and self.picture != dbInstance.picture:
            dbInstance.picture.delete(False)

        if self.picture:
            resize_picture(self.picture.path, self.picture.width, self.picture.height,
                self.picture_max_width, self.picture_max_height)

    def delete(self, using=None):
        super(Review, self).delete()

        if self.picture:
            try:
                self.picture.delete(False)
            except:
                pass
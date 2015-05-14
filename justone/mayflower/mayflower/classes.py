#coding:utf8
from itertools import ifilter
import os

from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image
from django.db.models import FileField
from redactor.fields import RedactorField


class SingleObjectModel(models.Model):
    class Meta:
        abstract = True

    def clean(self):
        if not self.pk and type(self).objects.exists():
            raise ValidationError(u'Можно создать только один объект данного класса')

    def delete(self, using=None):
        raise ValidationError(u'Нельзя удалять объекты данного класса')

    def __unicode__(self):
        if hasattr(self._meta, 'verbose_name'):
            return self._meta.verbose_name


class SEOModel(models.Model):
    class Meta:
        abstract = True

    page_title = models.TextField(verbose_name=u'Содержимое тега title', help_text=u'тег title')
    page_description = models.TextField(verbose_name=u'Содержимое description страницы', help_text=u'meta description', blank=True)
    page_keywords = models.TextField(verbose_name=u'Содержимое keywords страницы', help_text=u'meta keywords', blank=True)


class ThumbPictureModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def resize_picture(cls, image_path, width, height, max_width, max_height):
        if (max_width and width > max_width) or (max_height and height > max_height):
            img = Image.open(image_path).convert("RGB")
            img.thumbnail((max_width if max_width else width, max_height if max_height else height), Image.ANTIALIAS)
            img.save(image_path, quality=100)

    def _get_images_fields(self):
        return ifilter(lambda val: isinstance(val, models.ImageField), self._meta.fields)

    def save(self, *args, **kwargs):
        pictures_fields = {}

        for field in self._get_images_fields():
            max_width = getattr(self, field.name + '_max_width', None)
            max_height = getattr(self, field.name + '_max_height', None)

            if max_width or max_height:
                pictures_fields[field.name] = (max_width, max_height)

        db_instance = None

        if self.pk:
            try:
                db_instance = type(self).objects.get(pk=self.pk)
            except self.DoesNotExist:
                pass

        super(ThumbPictureModel, self).save(*args, **kwargs)

        for field_name, image_sizes in pictures_fields.iteritems():
            db_field_value = getattr(db_instance, field_name, None)
            field_value = getattr(self, field_name, None)

            if db_instance and db_field_value and db_field_value != field_value:
                db_field_value.delete(False)

            if field_value and os.path.exists(field_value.path):
                self.resize_picture(field_value.path, field_value.width, field_value.height, *image_sizes)

    def delete(self, using=None):
        super(ThumbPictureModel, self).delete()

        for base_field in self._get_images_fields():
            image_field = getattr(self, base_field.name, None)

            if image_field:
                try:
                    image_field.delete(False)
                except:
                    pass


class BasePageModel(SEOModel, SingleObjectModel):
    title = models.CharField(verbose_name=u'Заголовок', max_length=300, default='', blank=True)
    content = RedactorField(verbose_name=u'Контент')

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title or self.page_title

#coding:utf8
from datetime import date
import os
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
#from django.db.transaction import atomic
from redactor.fields import RedactorField

from mayflower.classes import SingleObjectModel, SEOModel, ThumbPictureModel


class BlogMainPage(SEOModel, SingleObjectModel):
    class Meta:
        verbose_name = u'настройки основной страницы блога'
        verbose_name_plural = u'настройки основной страницы блога'


class BlogTag(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=20, help_text=u'Максимум 20 символов')

    class Meta:
        verbose_name = u''
        verbose_name_plural = u'теги'

    def __unicode__(self):
        return self.name


class BlogItem(SEOModel, ThumbPictureModel):
    title = models.CharField(max_length=300, verbose_name=u'Заголовок', help_text=u'Максимум 300 символов')
    create_date = models.DateField(verbose_name=u'Дата создания', default=date.today, db_index=True)
    preview_image = models.ImageField(verbose_name=u'Preview-изображение', upload_to='blog_preview', blank=True,
                                      help_text=u'Если изображение не указано, то будет создано из детальной картинки')
    detail_image = models.ImageField(verbose_name=u'Детальное изображение', upload_to='blog_detail')

    content = RedactorField(verbose_name=u'Текст записи')
    tags = models.ManyToManyField(BlogTag, verbose_name=u'Теги', blank=True)

    preview_image_max_width = 200
    preview_image_max_height = 200

    detail_image_max_width = 720
    detail_image_max_height = 500

    class Meta:
        verbose_name = u'запись блога'
        verbose_name_plural = u'записи блога'

    def __unicode__(self):
        return self.title

    @property
    def url(self):
        return reverse('blog_detail', args=(self.id, ))

    def get_absolute_url(self):
        return self.url

    def save(self, *args, **kwargs):
#        with atomic():
        super(BlogItem, self).save(*args, **kwargs)

        if not self.preview_image:
            self.preview_image.save(os.path.basename(self.detail_image.url), File(open(self.detail_image.path)))
            # self.save()

#
# class BlogImage(models.Model):
#     blog_item = models.ForeignKey(BlogItem, verbose_name=u'Запись блога', related_name='extra_images')
#     image = models.ImageField(verbose_name=u'Изображение', upload_to='blog_extra_images')
#     name = models.CharField(verbose_name=u'Название изображения', max_length=300, default='', blank=True)
#
#     class Meta:
#         verbose_name = u'дополнительные изображение блога'
#         verbose_name_plural = u'изображения блога'
#
#     def __unicode__(self):
#         return u''
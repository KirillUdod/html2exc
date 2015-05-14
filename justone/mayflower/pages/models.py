#coding:utf8
from django.db import models
from django.template import Context, Template
from django.template.loader import render_to_string
from tinymce.models import HTMLField


class Page(models.Model):
    code = models.CharField(verbose_name=u'URL страницы', unique=True, max_length=500,
                            help_text=u'Если вы хотите, чтобы урл выглядел как"/test/", то в поле необходимо'
                                      u' указать "test/"')
    header = models.CharField(verbose_name=u'Заголовок страницы', max_length=300, help_text=u'Выводится в теге H1')
    title = models.CharField(verbose_name=u'Значение тега title', max_length=300)
    description = models.TextField(verbose_name=u'Значение description')
    keywords = models.TextField(verbose_name=u'Значение keywords')
    text = HTMLField(verbose_name=u'Контент страницы')

    class Meta:
        verbose_name = u'страница'
        verbose_name_plural = u'страницы'

    def __unicode__(self):
        return self.header

    @property
    def content_for_render(self):
        return u'{% load page_utils %}' + \
               self.text.replace(u'{%%20page_url%20', u'{% page_url ').replace(u'%20%}', u' %}')
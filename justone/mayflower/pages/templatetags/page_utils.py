#coding:utf8
from django import template
from django.core.urlresolvers import reverse
from django.template import Template, Variable, TemplateSyntaxError

from pages.models import Page

register = template.Library()


class RenderPageUrlNode(template.Node):
    def __init__(self, page_id):
        self.page_id = page_id

    def render(self, context):
        try:
            return reverse('page', args=(Page.objects.get(id=self.page_id).code, ))
        except Page.DoesNotExist:
            return ''


@register.tag
def page_url(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes only one argument"
                                  " (a variable representing a template to render)" % bits[0])

    try:
        page_id = int(bits[-1])
    except (ValueError, TypeError):
        raise TemplateSyntaxError("'%s' argument must be integer '%s' given" % bits)

    return RenderPageUrlNode(page_id)


class RenderAsTemplateNode(template.Node):
    def __init__(self, item_to_be_rendered):
        self.item_to_be_rendered = Variable(item_to_be_rendered)

    def render(self, context):
        try:
            actual_item = self.item_to_be_rendered.resolve(context)
            return Template(actual_item).render(context)
        except template.VariableDoesNotExist:
            return ''

@register.tag
def render_as_template(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes only one argument"
                                  " (a variable representing a template to render)" % bits[0])
    return RenderAsTemplateNode(bits[1])
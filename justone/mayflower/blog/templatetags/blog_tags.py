#coding:utf8
from django import template

register = template.Library()


@register.inclusion_tag('blog/request_path.html', takes_context=True)
def blog_path(context, page_num=None, tag_id=None, month=None, date=None):
    if date or month or tag_id:
        page_num = None
    else:
        page_num = page_num or context['page_obj'].number

    tag_id = tag_id or getattr(context.get('filter_tag'), 'id', None)
    month = month or context.get('filter_month')
    date = date or context.get('filter_date')

    return {
        'tag_id': tag_id,
        'page_num': page_num,
        'month': month,
        'date': date,
        'has_filter': tag_id or date or month
    }
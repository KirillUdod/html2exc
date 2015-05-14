#coding:utf8
from datetime import datetime, timedelta
from calendar import monthrange

from django.http import HttpResponseBadRequest
from django.views.generic import ListView, DetailView
from blog.models import BlogItem, BlogTag, BlogMainPage


def _get_tags_and_last_blogs():
    return {
        'last_blog_items': BlogItem.objects.only('title').order_by('-create_date')[:5],
        'tags': BlogTag.objects.all()
    }


class BlogListView(ListView):
    allow_empty = True
    template_name = 'blog/list.html'
    queryset = BlogItem.objects.only('create_date', 'title', 'preview_image').order_by('-create_date')
    paginate_by = 9
    page_kwarg = 'page'

    @staticmethod
    def chunks(l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

    def get(self, request, *args, **kwargs):
        extra_context = _get_tags_and_last_blogs()
        extra_context['blog_main_page'] = BlogMainPage.objects.get()
        self.object_list = self.get_queryset()


        if 'tag' in request.GET:
            try:
                blog_tag = BlogTag.objects.get(id=int(request.GET['tag']))
            except (BlogItem.DoesNotExist, ValueError, TypeError):
                return HttpResponseBadRequest()

            self.object_list = self.object_list.filter(tags=blog_tag)
            extra_context['filter_tag'] = blog_tag
        elif 'month' in request.GET:
            try:
                start_date = datetime.strptime(request.GET['month'], '%Y.%m').date()
            except ValueError:
                return HttpResponseBadRequest()

            end_date = start_date + timedelta(days=monthrange(start_date.year, start_date.month)[1])
            self.object_list = self.object_list.filter(create_date__range=(start_date, end_date))
            extra_context['filter_month'] = start_date
        elif 'date' in request.GET:
            try:
                filter_date = datetime.strptime(request.GET['date'], '%Y.%m.%d').date()
            except ValueError:
                return HttpResponseBadRequest()

            self.object_list = self.object_list.filter(create_date=filter_date)
            extra_context['filter_date'] = filter_date

        extra_context['object_list'] = self.object_list
        context = self.get_context_data(**extra_context)
        # сплитим весь список на списки по 1 элементy для рендеринга таблицы
        context['object_list'] = list(self.chunks(list(context['object_list']), 1))
        # if context['object_list'] and len(context['object_list'][-1]):
        #     context['object_list'][-1].extend([None] * (3 - len(context['object_list'][-1])))

        return self.render_to_response(context)


class BlogDetailView(DetailView):
    queryset = BlogItem.objects.select_related('tags', 'extra_images')
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'blog_id'

    def get_context_data(self, **kwargs):
        kwargs.update(_get_tags_and_last_blogs())
        return super(BlogDetailView, self).get_context_data(**kwargs)
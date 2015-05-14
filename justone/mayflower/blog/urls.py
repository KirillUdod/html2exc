from django.conf.urls import patterns, url

from blog.views import BlogDetailView, BlogListView

urlpatterns = patterns(
    'blog.views',
    url(r'^$', BlogListView.as_view(), name='blog_index'),
    url(r'^(?P<blog_id>\d+)/$', BlogDetailView.as_view(), name='blog_detail'),
)
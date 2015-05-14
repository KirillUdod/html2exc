#coding: utf-8
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url
    

urlpatterns = patterns(
    'walletone.views',
    url(
        r'^result/$',
        'receive_result',
        name='walletone_result'
    ),
    url(
        r'^success/$',
        'success_view',
        name='walletone_success'
    ),
    url(
        r'^fail/$',
        'fail_view',
        name='walletone_fail'
    ),
)

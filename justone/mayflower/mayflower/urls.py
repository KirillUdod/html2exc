#coding:utf8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from mayflower.views import PricesUpdateView

from walletone.urls import urlpatterns as payment_urls
from mayflower import settings

admin.autodiscover()


urlpatterns = patterns('mayflower.views',
    url(r'^$', 'home', name='home'),
    url(r'^(?P<category_type>special)/(?P<current_page>\d+)?$', 'catalog_category', name='special_subcategory_page'),
    url(r'^(?P<category_type>(unusual|bouquet|special))/$', 'index', name='category_page'),
    url(r'^(?P<category_type>(unusual|bouquet|special))/category_(?P<category_id>\d+)/(?P<current_page>\d+)?$', 'catalog_category', name='subcategory_page'),
    url(r'^(?P<category_type>(unusual|bouquet|special))/(?P<product_id>\d+)/$', 'index', name='product_page'),

    # url(r'^delivery/$', 'delivery', name='delivery'),
    url(r'^order/$', 'order', name='order'),
    url(r'^ordered/(?P<order_id>(\d+))/$', 'ordered', name='ordered'),
    url(r'^order/(?P<order_hash>([A-z0-9]+))/$', 'order_show', name='order_show'),

    url(r'^ajax_back_phone/$', 'back_call', name='back_call'),
    url(r'^ajax_basket_remove/$', 'remove_from_basket', name='remove_from_basket'),
    url(r'^ajax_basket_add/$', 'add_to_basket', name='add_to_basket'),

    url(r'^delivery_info/$', 'page', kwargs={'code': 'delivery'}, name='delivery_info'),
    url(r'^payment_info/$', 'page', kwargs={'code': 'pay'}, name='payment_info'),
    url(r'^encyclopedia_info/$', 'page', kwargs={'code': 'encyclopedia'}, name='encyclopedia_info'),
    #url(r'^payment/success/', 'mayflower.views.payment_success', name='payment_success'),
)

urlpatterns += patterns(
    '',
    url(r'^payment/', include(payment_urls)),

    url(r'^prices_update/$', PricesUpdateView.as_view(), name='bouquet_prices_update'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^mce_filebrowser/', include('mce_filebrowser.urls')),

    url(r'^blog/', include('blog.urls')),

    url(r'^redactor/', include('redactor.urls')),

    # должен быть всегда в конце
    url(r'(?P<page_code>[^?:&]+)', 'pages.views.show_page', name='page')
)


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
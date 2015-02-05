from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()


handler500 = handler404 = 'utils.views.handle404'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cart/', include('cart.urls')),
    url(r'^checkout/', include('checkout.urls')),
    url(r'^shops/', include('shops.urls')),
    url(r'^search/$', 'home.views.search', name='search'),
    url(r'^search/ajax/$', 'home.views.search_ajax', name='search.ajax'),
    url(r'^feedback/$', 'home.views.feedback', name='feedback'),
    url(r'^delivery/$', 'home.views.delivery'),
    url(r'^wholesale/$', 'home.views.wholesale'),
    url(r'^franchisee/credit/$', 'home.views.franchisee_credit'),
    url(r'^news/', include('news.urls')),
    url(r'^uploads/', include('uploads.urls')),
    url(r'^ideas/', include('ideas.urls')),
    url(r'^my/', include('users.urls')),
    url(r'^utils/', include('utils.urls')),
    url(r'^$', 'home.views.index', name='index'),
    url(r'^404/$', handler404),

    url(r'^rk-result/$', 'checkout.views.receive_result', name='robokassa_result'),
    url(r'^rk-success/$', 'checkout.views.success', name='robokassa_success'),
    url(r'^rk-fail/$', 'checkout.views.fail', name='robokassa_fail'),
    url(r'^payment-test/$', 'checkout.views.rk_test_start'),

    url(r'^internal/suggest/', include('django_select2.urls')),
    url(r'^internal/fastview/(?P<product_id>\d+)/$', 'products.views.products.fast_view'),
    url(r'^goods/\d+/-/(\d+)-.*/', 'products.views.products.legacy_redirect'),

    url(r'^new/$', 'products.views.categories.new'),
    url(r'', include('products.urls')),
    url(r'^captcha/', include('captcha.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf.urls import patterns, url


urlpatterns = patterns('users.views.auth',
    url(r'login/$', 'login', name='users.auth.login'),
    url(r'logout/$', 'logout', name='users.auth.logout'),
    url(r'register/$', 'register', name='users.auth.register'),
    url(r'register/wholesale/$', 'register_wholesale', name='users.auth.register.wholesale'),
    url(r'register/completed/$', 'registration_completed', name='users.auth.register.completed'),
    url(r'remind/$', 'remind', name='users.auth.remind'),
)

urlpatterns += patterns('users.views.addresses',
    url(r'^addresses/$', 'index', name='users.address.index'),
    url(r'^addresses/create/$', 'create', name='users.address.create'),
    url(r'^addresses/(?P<address_id>\d+)/update/$', 'update', name='users.address.update'),
    url(r'^addresses/(?P<address_id>\d+)/delete/$', 'delete', name='users.address.delete'),
)

urlpatterns += patterns('users.views.company',
    url(r'^company/update/$', 'update', name='users.company.update'),
)

urlpatterns += patterns('users.views.user',
    url(r'^$', lambda r: HttpResponseRedirect(reverse('users.user.update'))),
    url(r'^details/$', 'update', name='users.user.update'),
)

urlpatterns += patterns('users.views.orders',
    url(r'^orders/$', 'index', name='users.orders.index'),
    url(r'^orders/(?P<order_id>\d+)/$', 'read', name='users.orders.read'),
)

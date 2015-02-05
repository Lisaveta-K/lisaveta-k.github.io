# -*- coding: utf-8 -*-

from itertools import repeat

from djorm_pgfulltext.models import SearchManager
try:
    from django.utils.encoding import force_unicode as force_text
except ImportError:
    from django.utils.encoding import force_text
from django.db import models, connections, transaction


class ProductManager(SearchManager):

    def __init__(self):
        super(ProductManager, self).__init__(
            fields=('title', 'description'),
            config='pg_catalog.russian',
            auto_update_search_field=True,
        )

    def search(self, *args, **kwargs):
        user = kwargs.pop('user')

        qs = super(ProductManager, self).search(*args, **kwargs)
        return self._prepare(qs, user)

    def for_user(self, user):
        qs = super(ProductManager, self).get_queryset()
        return self._prepare(qs, user)

    @staticmethod
    def _prepare(qs, user):
        if user.is_anonymous() or (user.is_customer or user.is_staff):
            qs = qs.filter(is_retail=True, quantity__gt=0)
        elif user.show_wholesale():
            qs = qs.filter(is_wholesale=True, wholesale_quantity__gt=0)

        if user.is_authenticated():
            if user.is_wholesale:
                qs = qs.filter(wholesale_price__gt=0)
            elif user.is_franchisee:
                qs = qs.filter(franchisee_price__gt=0)
            else:
                qs = qs.filter(price__gt=0)

        return qs.filter(is_visible=True)


    def update_search_field(self, pk=None, config=None, using=None):
        '''
        Update the search_field of one instance, or a list of instances, or
        all instances in the table (pk is one key, a list of keys or none).

        If there is no search_field, this function does nothing.


        Пришлось перегрузить метод, чтобы убрать транзакции.
        см. https://github.com/niwibe/djorm-ext-pgfulltext/issues/10
        '''

        if not self.search_field:
            return

        if not config:
            config = self.config

        if using is None:
            using = self.db

        connection = connections[using]
        qn = connection.ops.quote_name

        where_sql = ''
        params = []
        if pk is not None:
            if isinstance(pk, (list, tuple)):
                params = pk
            else:
                params = [pk]

            where_sql = "WHERE %s IN (%s)" % (
                qn(self.model._meta.pk.column),
                ','.join(repeat("%s", len(params)))
            )

        search_vector = self._get_search_vector(config, using)
        sql = "UPDATE %s SET %s = %s %s;" % (
            qn(self.model._meta.db_table),
            qn(self.search_field),
            search_vector,
            where_sql
        )

        #if not transaction.is_managed(using=using):
        #    transaction.enter_transaction_management(using=using)
        #    forced_managed = True
        #else:
        #    forced_managed = False

        cursor = connection.cursor()
        cursor.execute(sql, params)

        #try:
        #    if forced_managed:
        #        transaction.commit(using=using)
        #    else:
        #        transaction.commit_unless_managed(using=using)
        #finally:
        #    if forced_managed:
        #        transaction.leave_transaction_management(using=using)
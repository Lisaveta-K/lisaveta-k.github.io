# -*- coding: utf-8 -*-

import datetime

from django.db import models


class CouponManager(models.Manager):

    def actual(self, code):
        today = datetime.date.today()

        return self.get_queryset().get(code=code, date_start__lte=today, date_end__gte=today)

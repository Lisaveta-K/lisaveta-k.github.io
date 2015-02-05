# -*- coding: utf-8 -*-

import datetime

from django.db import models

from users.models import User, Address
from products.models import Product
from shops.models import Delivery, Shop, Discount
from adverts.models import Coupon


class OrderItem(models.Model):
    order = models.ForeignKey('checkout.Order')
    product = models.ForeignKey(Product, null=True, blank=True, verbose_name=u'Товар')
    product_legacy_id = models.PositiveIntegerField(editable=False, default=0)
    amount = models.PositiveIntegerField(u'Количество', default=1)
    per_item = models.DecimalField(u'Цена за штуку', max_digits=8, decimal_places=2)
    sign = models.TextField(u'Подпись к товару', blank=True)

    @property
    def quantity(self):
        return self.amount

    @property
    def net(self):
        return self.amount * self.per_item


class Order(models.Model):
    STATUS_RECEIVED = 0
    STATUS_PAYMENT_WAITING = 1
    STATUS_PAYED = 2
    STATUS_PROCESSING = 3
    STATUS_SENDED = 4
    STATUS_CANCELED = 5

    STATUS_CHOICES = (
        (STATUS_RECEIVED, u'Принят'),
        (STATUS_PAYMENT_WAITING, u'Ожидает оплаты'),
        (STATUS_PAYED, u'Оплачен'),
        (STATUS_PROCESSING, u'В обработке'),
        (STATUS_SENDED, u'Отправлен'),
        (STATUS_CANCELED, u'Отменен'),
    )

    PAYMENT_ROBOKASSA = 0  # Оплата через Робокассу
    PAYMENT_CASHPICK = 1  # Наличными при самовывозе
    PAYMENT_COURIER = 2  # Курьеру
    PAYMENT_CASHLESS = 3 # Безналичный расчет

    PAYMENT_CHOICES = (
        (PAYMENT_ROBOKASSA, u'Робокасса'),
        (PAYMENT_CASHPICK, u'Наличными'),
        (PAYMENT_COURIER, u'Курьеру'),
        (PAYMENT_CASHLESS, u'Безналичный расчет'),
    )

    user = models.ForeignKey(User, related_name='orders', null=True, blank=True, verbose_name=u'Пользователь')
    address = models.ForeignKey(Address, related_name='orders', null=True, blank=True, verbose_name=u'Адрес')
    delivery_date = models.DateField(u'Дата доставки', default=None, null=True, blank=True)
    delivery_time = models.TimeField(u'Время доставки', default=None, null=True, blank=True)
    shop = models.ForeignKey(Shop, related_name='orders', null=True, blank=True, verbose_name=u'Магазин')
    status = models.PositiveSmallIntegerField(u'Статус', choices=STATUS_CHOICES, default=STATUS_RECEIVED)
    products_price = models.DecimalField(u'Стоимость товаров без скидок', default=0, max_digits=8, decimal_places=2)
    net = models.DecimalField(u'Сумма заказа', default=0, max_digits=8, decimal_places=2)  # с доставкой и скидками
    code = models.CharField(max_length=10)
    delivery = models.ForeignKey(Delivery, null=True, blank=True, verbose_name=u'Доставка')
    delivery_cost = models.PositiveIntegerField(u'Стоимость доставки', default=0)
    payment_type = models.PositiveSmallIntegerField(u'Оплата', choices=PAYMENT_CHOICES, null=True, blank=True)
    discount = models.ForeignKey(Discount, null=True, blank=True, verbose_name=u'Скидка')
    coupon = models.ForeignKey(Coupon, null=True, blank=True, verbose_name=u'Промо-код')
    comment = models.TextField(u'Комментарий', blank=True)
    products = models.ManyToManyField(Product, through=OrderItem)
    created = models.DateTimeField(u'Дата создания', default=datetime.datetime.now)
    is_emails_sended = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'заказ'
        verbose_name_plural = u'заказы'

    def __unicode__(self):
        return u'Заказ №%s' % self.id

    @property
    def products_cost(self):
        return self.net - self.delivery_cost

    @property
    def coupon_price(self):
        return self.products_price - self.net


class CourierCity(models.Model):
    title = models.CharField(u'Название', max_length=255)
    price = models.PositiveIntegerField(u'Цена')

    class Meta:
        verbose_name = u'город курьерской доставки'
        verbose_name_plural = u'город курьерской доставки'

    def __unicode__(self):
        return self.title

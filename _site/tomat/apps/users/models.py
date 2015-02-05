# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from users.managers import UserManager


class User(AbstractBaseUser):
    """Покупатель"""

    STATUS_ADMIN = 0
    STATUS_CUSTOMER = 1
    STATUS_WHOLESALE = 2
    STATUS_FRANCHISEE = 3

    STATUS_CHOICES = (
        (STATUS_ADMIN, u'Администратор'),
        (STATUS_CUSTOMER, u'Розничный покупатель'),
        (STATUS_WHOLESALE, u'Оптовый покупатель'),
        (STATUS_FRANCHISEE, u'Франчайзи'),
    )

    email = models.EmailField(u'E-mail', unique=True, db_index=True)
    is_active = models.BooleanField(default=False, db_index=True)
    title = models.CharField(u'ФИО', max_length=255, blank=True)
    phone = models.CharField(u'Телефон', max_length=50, blank=True)
    birthday = models.DateField(u'Дата рождения', blank=True, null=True)
    status = models.PositiveSmallIntegerField(u'Тип', choices=STATUS_CHOICES, default=STATUS_CUSTOMER,
        db_index=True)
    created = models.DateTimeField(u'Дата регистрации', default=datetime.datetime.now)

    objects = UserManager()

    class Meta:
        db_table = u'users_user'
        verbose_name = u'пользователь'
        verbose_name_plural = u'пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    def get_full_name(self):
        return self.title

    def get_short_name(self):
        return self.title

    @property
    def is_staff(self):
        return self.status == self.STATUS_ADMIN

    @property
    def is_customer(self):
        return self.status == self.STATUS_CUSTOMER

    @property
    def is_wholesale(self):
        return self.status == self.STATUS_WHOLESALE

    @property
    def is_franchisee(self):
        return self.status == self.STATUS_FRANCHISEE

    def show_wholesale(self):
        return self.status in (self.STATUS_WHOLESALE, self.STATUS_FRANCHISEE)

    def has_perm(self, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if self.status == self.STATUS_ADMIN:
            self.is_active = True
        return super(User, self).save(*args, **kwargs)


class Country(models.Model):
    title = models.CharField(u'Название', max_length=50)


class Region(models.Model):
    country = models.ForeignKey(Country)
    title = models.CharField(u'Название', max_length=255)


class City(models.Model):
    region = models.ForeignKey(Region)
    title = models.CharField(u'Название', max_length=255)

    def __unicode__(self):
        return self.title


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses')
    city = models.CharField(u'Город', max_length=255, blank=True)
    postal_code = models.CharField(u'Индекс', max_length=6, blank=True)
    street = models.CharField(u'Улица', max_length=255, blank=True)
    house = models.CharField(u'Дом, корпус, строение', max_length=255, blank=True)
    flat = models.CharField(u'Квартира, офис', max_length=255, blank=True)
    original_string = models.TextField(u'Адрес со старого сайта', blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(u'Контактный телефон', max_length=255, blank=True)
    courier_city = models.ForeignKey('checkout.CourierCity', null=True, blank=True)

    receiver_title = models.CharField(u'ФИО получателя', max_length=255)
    receiver_phone = models.CharField(u'Телефон получателя', max_length=255, blank=True)
    is_deleted = models.BooleanField(u'Удален', default=False)

    class Meta:
        verbose_name = u'адрес'
        verbose_name_plural = u'адреса'

    def __unicode__(self):
        bits = [self.postal_code, self.city, self.street, self.house, self.flat]

        return u', '.join([x for x in bits if x])


class Company(models.Model):
    user = models.OneToOneField(User, related_name='company')
    title = models.CharField(u'Название', max_length=255, blank=True)
    city = models.CharField(u'Город', max_length=255, blank=True)
    industry = models.CharField(u'Занятия', max_length=255, blank=True)
    phone = models.CharField(u'Телефон', max_length=255)
    inn = models.CharField(u'ИНН/КПП', max_length=25, blank=True)
    ogrn = models.CharField(u'ОГРН', max_length=15, blank=True)
    giro = models.CharField(u'Расчетный счет', max_length=25, blank=True)
    juridical_address = models.TextField(u'Юридический адрес', blank=True)
    post_address = models.TextField(u'Почтовый адрес', blank=True)
    phone = models.CharField(u'Телефон', max_length=255, blank=True)
    director = models.CharField(u'Контактное лицо', max_length=255)

    class Meta:
        verbose_name = u'компания'
        verbose_name_plural = u'компания'

    def __unicode__(self):
        return self.title

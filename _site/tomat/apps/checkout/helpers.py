# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from checkout.models import OrderItem, Order

def send_order_mails(order, user):
    items = OrderItem.objects.filter(order=order).select_related('product')

    context = {
        'order': order,
        'items': items,
    }

    if not user.has_usable_password():
        password = get_random_string(5, 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789').upper()
        context['password'] = password
        user.set_password(password)
        user.save()

    manager_text = render_to_string('checkout/mail/manager.txt', context)
    manager_html = render_to_string('checkout/mail/manager.html', context)
    mail_managers(u'Новый заказ №%d от %s' % (order.id, order.created.strftime('%d.%m.%Y %H:%M')),
        manager_text, html_message=manager_html)

    user_text = render_to_string('checkout/mail/user.txt', context)
    user_html = render_to_string('checkout/mail/user.html', context)
    message = EmailMultiAlternatives(u'Ваш заказ №%d в интернет-магазине «Томат»' % order.id, user_text,
        settings.EMAIL_FROM, [user.email, ])
    message.attach_alternative(user_html, 'text/html')
    message.send()

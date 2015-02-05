# -*- coding: utf-8 -*-

import logging


logger = logging.getLogger(__name__)


def payment_received(sender, **kwargs):
    from checkout.models import Order

    order = Order.objects.get(id=kwargs['InvId'])
    order.status = Order.STATUS_PAYED
    order.net = kwargs['OutSum']
    logger.info('Order #%d had payed. Sum: %s' % (order.id, order.net))
    order.save()


def payment_failed(sender, **kwargs):
    logger.error('Payment for order #%d failed' % kwargs['InvId'])

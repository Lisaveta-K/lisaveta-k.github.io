# -*- coding: utf-8 -*-
import datetime


def is_holiday(_date):
    """Является ли заданная дата выходным днём"""
    return _date.weekday() == 5 or _date.weekday() == 6


def get_nearest_monday(_date):
    """Ближайший понедельник к заданной дате"""
    days_ahead = 0 - _date.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return (_date + datetime.timedelta(days_ahead)).replace(hour=10, minute=0)


def is_friday_after_six_oclock(_date):
    return _date.weekday() == 4 and _date.hour >= 18


def combine_date_and_time(_date, _time):
    if not _date:
        return None
    if not _time:
        _time = datetime.time(0, 0, 0)
    return datetime.datetime.combine(_date, _time)

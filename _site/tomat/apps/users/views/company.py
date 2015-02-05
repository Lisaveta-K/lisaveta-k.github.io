# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect

from users.models import Company
from users.forms import CompanyForm


def update(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:  # Для старых компаний
        company = Company()

    if request.POST:
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('.')

    else:
        form = CompanyForm(instance=company)

    context = {
        'form': form,
    }

    return render(request, 'users/company/update.html', context)

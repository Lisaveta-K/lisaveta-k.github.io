# -*- coding: utf-8 -*-

from django.contrib import admin

from home.models import Feedback, Link


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('_title', 'created')
    list_select_related = True
    readonly_fields = ('user', 'email', 'title', 'content', 'created')

    def _title(self, obj):
        if obj.user_id:
            return obj.user.email
        return u'%s <%s>' % (obj.title, obj.email)
    _title.short_description = u'Имя пользователя'

admin.site.register(Feedback, FeedbackAdmin)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'position')
    list_editable = ('position',)

admin.site.register(Link, LinkAdmin)

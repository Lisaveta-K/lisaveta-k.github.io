# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'News.preview'
        db.add_column(u'news_news', 'preview',
                      self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'News.preview'
        db.delete_column(u'news_news', 'preview')


    models = {
        u'news.news': {
            'Meta': {'object_name': 'News'},
            'caption': ('django.db.models.fields.TextField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_published': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['news']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Discount'
        db.create_table(u'shops_discount', (
            ('id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('percent', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'shops', ['Discount'])


    def backwards(self, orm):
        # Deleting model 'Discount'
        db.delete_table(u'shops_discount')


    models = {
        u'shops.city': {
            'Meta': {'object_name': 'City', 'db_table': "'shops_cities'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'shops.delivery': {
            'Meta': {'object_name': 'Delivery'},
            'caption': ('django.db.models.fields.TextField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'shops.discount': {
            'Meta': {'object_name': 'Discount'},
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'percent': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'shops.shop': {
            'Meta': {'object_name': 'Shop'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shops'", 'to': u"orm['shops.City']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phones': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'worktime': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['shops']
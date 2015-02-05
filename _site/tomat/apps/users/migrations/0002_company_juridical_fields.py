# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Company.inn'
        db.add_column(u'users_company', 'inn',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=25),
                      keep_default=False)

        # Adding field 'Company.ogrn'
        db.add_column(u'users_company', 'ogrn',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=13),
                      keep_default=False)

        # Adding field 'Company.giro'
        db.add_column(u'users_company', 'giro',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=25),
                      keep_default=False)

        # Adding field 'Company.juridical_address'
        db.add_column(u'users_company', 'juridical_address',
                      self.gf('django.db.models.fields.TextField')(default=None),
                      keep_default=False)

        # Adding field 'Company.post_address'
        db.add_column(u'users_company', 'post_address',
                      self.gf('django.db.models.fields.TextField')(default=None),
                      keep_default=False)

        # Adding field 'Company.director'
        db.add_column(u'users_company', 'director',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Company.inn'
        db.delete_column(u'users_company', 'inn')

        # Deleting field 'Company.ogrn'
        db.delete_column(u'users_company', 'ogrn')

        # Deleting field 'Company.giro'
        db.delete_column(u'users_company', 'giro')

        # Deleting field 'Company.juridical_address'
        db.delete_column(u'users_company', 'juridical_address')

        # Deleting field 'Company.post_address'
        db.delete_column(u'users_company', 'post_address')

        # Deleting field 'Company.director'
        db.delete_column(u'users_company', 'director')


    models = {
        u'users.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'flat': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_string': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'receiver_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'to': u"orm['users.User']"})
        },
        u'users.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Region']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'giro': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'juridical_address': ('django.db.models.fields.TextField', [], {}),
            'ogrn': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'post_address': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'company'", 'unique': 'True', 'to': u"orm['users.User']"})
        },
        u'users.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'users.region': {
            'Meta': {'object_name': 'Region'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['users']
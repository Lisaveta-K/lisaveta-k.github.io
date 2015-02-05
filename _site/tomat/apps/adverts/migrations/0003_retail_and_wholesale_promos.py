# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    no_dry_run = True

    def forwards(self, orm):
        # Adding field 'Promo.is_retail'
        db.add_column('adverts_promos', 'is_retail',
                      self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True),
                      keep_default=False)

        from django.db import connection
        cursor = connection.cursor()

        cursor.execute('UPDATE adverts_promos SET is_retail = is_visible;')
        connection.commit()

        # Adding field 'Promo.is_wholesale'
        db.add_column('adverts_promos', 'is_wholesale',
                      self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True),
                      keep_default=False)

        db.delete_column('adverts_promos', 'is_visible')


    def backwards(self, orm):
        # Deleting field 'Promo.is_retail'
        db.delete_column('adverts_promos', 'is_retail')

        # Deleting field 'Promo.is_wholesale'
        db.delete_column('adverts_promos', 'is_wholesale')

        db.add_column('adverts_promos', 'is_visible',
            self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True),
            keep_default=False)

    models = {
        u'adverts.promo': {
            'Meta': {'object_name': 'Promo', 'db_table': "'adverts_promos'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'promos'", 'null': 'True', 'to': u"orm['products.Category']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_retail': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_wholesale': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'products.category': {
            'Meta': {'object_name': 'Category', 'db_table': "'products_categories'"},
            'complementary_cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'complementary_hover_cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complementary': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_standalone': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'legacy_id': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['products.Category']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'show_cover_in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['adverts']

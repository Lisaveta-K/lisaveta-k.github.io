# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    no_dry_run = True

    def forwards(self, orm):

        # Adding M2M table for field categories on 'Promo'
        db.create_table('adverts_promos_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('promo', models.ForeignKey(orm[u'adverts.promo'], null=False)),
            ('category', models.ForeignKey(orm[u'products.category'], null=False))
        ))
        db.create_unique('adverts_promos_categories', ['promo_id', 'category_id'])

        from django.db import connection, transaction
        cursor = connection.cursor()

        for promo in orm['adverts.Promo'].objects.all():
            cursor.execute('SELECT category_id FROM adverts_promos WHERE id = %s', [promo.id, ])
            category_id = cursor.fetchone()[0]
            if category_id:
                cursor.execute('INSERT INTO adverts_promos_categories (promo_id, category_id) VALUES (%s, %s);', [promo.id, category_id])
                transaction.commit()

        # Deleting field 'Promo.category'
        db.delete_column('adverts_promos', 'category_id')


    def backwards(self, orm):
        # Adding field 'Promo.category'
        db.add_column('adverts_promos', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='promos', null=True, to=orm['products.Category'], blank=True),
                      keep_default=False)

        # Removing M2M table for field categories on 'Promo'
        db.delete_table('adverts_promos_categories')


    models = {
        u'adverts.promo': {
            'Meta': {'object_name': 'Promo', 'db_table': "'adverts_promos'"},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'promos'", 'blank': 'True', 'to': u"orm['products.Category']"}),
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
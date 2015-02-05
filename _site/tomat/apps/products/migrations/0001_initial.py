# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('products_categories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['products.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('is_complementary', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_standalone', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('legacy_id', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=255, null=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'products', ['Category'])

        # Adding model 'Product'
        db.create_table('products_items', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=30, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=8, decimal_places=2, blank=True)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('wholesale_price', self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=8, decimal_places=2, blank=True)),
            ('wholesale_discount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('franchisee_price', self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=8, decimal_places=2, blank=True)),
            ('franchisee_discount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_new', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_wholesale', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('weight', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('dimensions', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('pack_amount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('quantity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('wholesale_legacy_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'products', ['Product'])

        # Adding M2M table for field categories on 'Product'
        db.create_table('products_items_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'products.product'], null=False)),
            ('category', models.ForeignKey(orm[u'products.category'], null=False))
        ))
        db.create_unique('products_items_categories', ['product_id', 'category_id'])

        # Adding model 'Photo'
        db.create_table('products_photos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', to=orm['products.Product'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('is_main', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('legacy_hash', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'products', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('products_categories')

        # Deleting model 'Product'
        db.delete_table('products_items')

        # Removing M2M table for field categories on 'Product'
        db.delete_table('products_items_categories')

        # Deleting model 'Photo'
        db.delete_table('products_photos')


    models = {
        u'products.category': {
            'Meta': {'object_name': 'Category', 'db_table': "'products_categories'"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complementary': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_standalone': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'legacy_id': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['products.Category']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'products.photo': {
            'Meta': {'object_name': 'Photo', 'db_table': "'products_photos'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_main': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'legacy_hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': u"orm['products.Product']"})
        },
        u'products.product': {
            'Meta': {'object_name': 'Product', 'db_table': "'products_items'"},
            'categories': ('mptt.fields.TreeManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'to': u"orm['products.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dimensions': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'franchisee_discount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'franchisee_price': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_wholesale': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'pack_amount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'price': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'sku': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wholesale_discount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'wholesale_legacy_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'wholesale_price': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'})
        }
    }

    complete_apps = ['products']
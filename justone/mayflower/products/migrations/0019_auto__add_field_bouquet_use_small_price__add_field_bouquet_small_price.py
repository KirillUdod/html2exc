# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bouquet.use_small_price'
        db.add_column(u'products_bouquet', 'use_small_price',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Bouquet.small_price'
        db.add_column(u'products_bouquet', 'small_price',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bouquet.small_old_price'
        db.add_column(u'products_bouquet', 'small_old_price',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bouquet.small_description'
        db.add_column(u'products_bouquet', 'small_description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Bouquet.use_big_price'
        db.add_column(u'products_bouquet', 'use_big_price',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Bouquet.big_price'
        db.add_column(u'products_bouquet', 'big_price',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bouquet.big_old_price'
        db.add_column(u'products_bouquet', 'big_old_price',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bouquet.big_description'
        db.add_column(u'products_bouquet', 'big_description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Bouquet.use_small_price'
        db.delete_column(u'products_bouquet', 'use_small_price')

        # Deleting field 'Bouquet.small_price'
        db.delete_column(u'products_bouquet', 'small_price')

        # Deleting field 'Bouquet.small_old_price'
        db.delete_column(u'products_bouquet', 'small_old_price')

        # Deleting field 'Bouquet.small_description'
        db.delete_column(u'products_bouquet', 'small_description')

        # Deleting field 'Bouquet.use_big_price'
        db.delete_column(u'products_bouquet', 'use_big_price')

        # Deleting field 'Bouquet.big_price'
        db.delete_column(u'products_bouquet', 'big_price')

        # Deleting field 'Bouquet.big_old_price'
        db.delete_column(u'products_bouquet', 'big_old_price')

        # Deleting field 'Bouquet.big_description'
        db.delete_column(u'products_bouquet', 'big_description')


    models = {
        u'products.bouquet': {
            'Meta': {'object_name': 'Bouquet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'big_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'big_old_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'big_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['products.BouquetCategory']", 'through': u"orm['products.BouquetCategoryThrough']", 'symmetrical': 'False'}),
            'category_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'old_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'one_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'show_in_bouquets': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_in_unusuals': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slider_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'small_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'small_old_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'small_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'use_big_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_small_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'products.bouquetcategory': {
            'Meta': {'object_name': 'BouquetCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'show_on_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slider_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'use_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'products.bouquetcategorythrough': {
            'Meta': {'object_name': 'BouquetCategoryThrough'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.BouquetCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Bouquet']"}),
            'sort': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'})
        },
        u'products.bouquetprice': {
            'Meta': {'unique_together': "(('product', 'height', 'count'),)", 'object_name': 'BouquetPrice'},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'old_price': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Bouquet']"})
        },
        u'products.review': {
            'Meta': {'object_name': 'Review'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'products.special': {
            'Meta': {'object_name': 'Special'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'old_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'show_in_bouquets': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_in_unusuals': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slider_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'use_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'products.unusual': {
            'Meta': {'object_name': 'Unusual'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['products.UnusualCategory']", 'through': u"orm['products.UnusualCategoryThrough']", 'symmetrical': 'False'}),
            'category_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'old_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'show_in_bouquets': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_in_unusuals': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slider_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'use_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'products.unusualcategory': {
            'Meta': {'object_name': 'UnusualCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'show_on_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slider_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'use_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'products.unusualcategorythrough': {
            'Meta': {'object_name': 'UnusualCategoryThrough'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.UnusualCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Unusual']"}),
            'sort': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'})
        }
    }

    complete_apps = ['products']
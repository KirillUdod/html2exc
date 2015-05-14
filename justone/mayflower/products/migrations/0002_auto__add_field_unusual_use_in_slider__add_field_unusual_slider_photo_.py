# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Unusual.use_in_slider'
        db.add_column(u'products_unusual', 'use_in_slider',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Unusual.slider_photo'
        db.add_column(u'products_unusual', 'slider_photo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bouquet.use_in_slider'
        db.add_column(u'products_bouquet', 'use_in_slider',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Bouquet.slider_photo'
        db.add_column(u'products_bouquet', 'slider_photo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Special.use_in_slider'
        db.add_column(u'products_special', 'use_in_slider',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Special.slider_photo'
        db.add_column(u'products_special', 'slider_photo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Unusual.use_in_slider'
        db.delete_column(u'products_unusual', 'use_in_slider')

        # Deleting field 'Unusual.slider_photo'
        db.delete_column(u'products_unusual', 'slider_photo')

        # Deleting field 'Bouquet.use_in_slider'
        db.delete_column(u'products_bouquet', 'use_in_slider')

        # Deleting field 'Bouquet.slider_photo'
        db.delete_column(u'products_bouquet', 'slider_photo')

        # Deleting field 'Special.use_in_slider'
        db.delete_column(u'products_special', 'use_in_slider')

        # Deleting field 'Special.slider_photo'
        db.delete_column(u'products_special', 'slider_photo')


    models = {
        u'products.bouquet': {
            'Meta': {'object_name': 'Bouquet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': u"orm['products.BouquetCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'old_price_101': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'old_price_25': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'old_price_51': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'old_price_81': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'price_101': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price_25': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price_51': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price_81': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slider_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'small_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'use_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'products.bouquetcategory': {
            'Meta': {'object_name': 'BouquetCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
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
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'old_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slider_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'small_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'use_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'products.unusual': {
            'Meta': {'object_name': 'Unusual'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': u"orm['products.UnusualCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'old_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slider_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'small_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'use_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'products.unusualcategory': {
            'Meta': {'object_name': 'UnusualCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['products']
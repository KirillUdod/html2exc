# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bouquet.one_price'
        db.add_column(u'products_bouquet', 'one_price',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Bouquet.price'
        db.add_column(u'products_bouquet', 'price',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Bouquet.price_51'
        db.alter_column(u'products_bouquet', 'price_51', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'Bouquet.price_25'
        db.alter_column(u'products_bouquet', 'price_25', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'Bouquet.price_81'
        db.alter_column(u'products_bouquet', 'price_81', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'Bouquet.price_101'
        db.alter_column(u'products_bouquet', 'price_101', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Bouquet.one_price'
        db.delete_column(u'products_bouquet', 'one_price')

        # Deleting field 'Bouquet.price'
        db.delete_column(u'products_bouquet', 'price')


        # User chose to not deal with backwards NULL issues for 'Bouquet.price_51'
        raise RuntimeError("Cannot reverse this migration. 'Bouquet.price_51' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Bouquet.price_51'
        db.alter_column(u'products_bouquet', 'price_51', self.gf('django.db.models.fields.PositiveIntegerField')())

        # User chose to not deal with backwards NULL issues for 'Bouquet.price_25'
        raise RuntimeError("Cannot reverse this migration. 'Bouquet.price_25' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Bouquet.price_25'
        db.alter_column(u'products_bouquet', 'price_25', self.gf('django.db.models.fields.PositiveIntegerField')())

        # User chose to not deal with backwards NULL issues for 'Bouquet.price_81'
        raise RuntimeError("Cannot reverse this migration. 'Bouquet.price_81' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Bouquet.price_81'
        db.alter_column(u'products_bouquet', 'price_81', self.gf('django.db.models.fields.PositiveIntegerField')())

        # User chose to not deal with backwards NULL issues for 'Bouquet.price_101'
        raise RuntimeError("Cannot reverse this migration. 'Bouquet.price_101' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Bouquet.price_101'
        db.alter_column(u'products_bouquet', 'price_101', self.gf('django.db.models.fields.PositiveIntegerField')())

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
            'one_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_101': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_25': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_51': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_81': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
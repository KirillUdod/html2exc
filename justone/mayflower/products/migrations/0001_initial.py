# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BouquetCategory'
        db.create_table(u'products_bouquetcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'products', ['BouquetCategory'])

        # Adding model 'Bouquet'
        db.create_table(u'products_bouquet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('small_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['products.BouquetCategory'])),
            ('price_25', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price_51', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price_81', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price_101', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('old_price_25', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('old_price_51', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('old_price_81', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('old_price_101', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'products', ['Bouquet'])

        # Adding model 'UnusualCategory'
        db.create_table(u'products_unusualcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'products', ['UnusualCategory'])

        # Adding model 'Unusual'
        db.create_table(u'products_unusual', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('small_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('old_price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['products.UnusualCategory'])),
        ))
        db.send_create_signal(u'products', ['Unusual'])

        # Adding model 'Special'
        db.create_table(u'products_special', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('small_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('old_price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'products', ['Special'])

        # Adding model 'Review'
        db.create_table(u'products_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'products', ['Review'])



    def backwards(self, orm):
        # Deleting model 'BouquetCategory'
        db.delete_table(u'products_bouquetcategory')

        # Deleting model 'Bouquet'
        db.delete_table(u'products_bouquet')

        # Deleting model 'UnusualCategory'
        db.delete_table(u'products_unusualcategory')

        # Deleting model 'Unusual'
        db.delete_table(u'products_unusual')

        # Deleting model 'Special'
        db.delete_table(u'products_special')

        # Deleting model 'Review'
        db.delete_table(u'products_review')


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
            'small_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
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
            'small_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
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
            'small_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'products.unusualcategory': {
            'Meta': {'object_name': 'UnusualCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['products']
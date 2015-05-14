# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Order.add_card_congrats'
        db.delete_column(u'order_order', 'add_card_congrats')

        # Deleting field 'Order.add_card_birthday'
        db.delete_column(u'order_order', 'add_card_birthday')

        # Deleting field 'Order.add_card_love'
        db.delete_column(u'order_order', 'add_card_love')

        # Adding field 'Order.add_card'
        db.add_column(u'order_order', 'add_card',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Order.pay_for_delivery_date'
        db.add_column(u'order_order', 'pay_for_delivery_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Order.pay_for_delivery_time'
        db.add_column(u'order_order', 'pay_for_delivery_time',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Order.pay_for_delivery_address'
        db.add_column(u'order_order', 'pay_for_delivery_address',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Order.add_card_congrats'
        db.add_column(u'order_order', 'add_card_congrats',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Order.add_card_birthday'
        db.add_column(u'order_order', 'add_card_birthday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Order.add_card_love'
        db.add_column(u'order_order', 'add_card_love',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Order.add_card'
        db.delete_column(u'order_order', 'add_card')

        # Deleting field 'Order.pay_for_delivery_date'
        db.delete_column(u'order_order', 'pay_for_delivery_date')

        # Deleting field 'Order.pay_for_delivery_time'
        db.delete_column(u'order_order', 'pay_for_delivery_time')

        # Deleting field 'Order.pay_for_delivery_address'
        db.delete_column(u'order_order', 'pay_for_delivery_address')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'order.basket': {
            'Meta': {'object_name': 'Basket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'basket'", 'null': 'True', 'to': u"orm['order.Order']"}),
            'product_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'product_price': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['products.BouquetPrice']", 'null': 'True', 'blank': 'True'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'order.order': {
            'Meta': {'object_name': 'Order'},
            'add_card': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'add_toy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'anonymous_delivery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clarify_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'customer_is_destination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_date': ('django.db.models.fields.DateField', [], {}),
            'delivery_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'delivery_time': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'delivery_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'destination_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'destination_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'destination_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'make_photo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'order_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pay_for_delivery_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'pay_for_delivery_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'pay_for_delivery_time': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pay_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'pay_type_old': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'positions': ('django.db.models.fields.TextField', [], {}),
            'send_sms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'products.bouquet': {
            'Meta': {'object_name': 'Bouquet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'use_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'products.bouquetcategory': {
            'Meta': {'object_name': 'BouquetCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'show_on_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sort': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'})
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
        }
    }

    complete_apps = ['order']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Basket'
        db.create_table(u'order_basket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='basket', null=True, to=orm['order.Order'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('product_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'order', ['Basket'])

        # Adding model 'Order'
        db.create_table(u'order_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_hash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('order_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pay_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('clarify_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('customer_is_destination', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('destination_name', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('destination_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('destination_phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('delivery_time', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('delivery_date', self.gf('django.db.models.fields.DateField')()),
            ('delivery_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('delivery_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('positions', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'order', ['Order'])


    def backwards(self, orm):
        # Deleting model 'Basket'
        db.delete_table(u'order_basket')

        # Deleting model 'Order'
        db.delete_table(u'order_order')


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
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'order.order': {
            'Meta': {'object_name': 'Order'},
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'order_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pay_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'positions': ('django.db.models.fields.TextField', [], {}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['order']
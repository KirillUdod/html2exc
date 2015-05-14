# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaymentNotification'
        db.create_table(u'walletone_paymentnotification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order_id', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('merchant_order_id', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'walletone', ['PaymentNotification'])


    def backwards(self, orm):
        # Deleting model 'PaymentNotification'
        db.delete_table(u'walletone_paymentnotification')


    models = {
        u'walletone.paymentnotification': {
            'Meta': {'object_name': 'PaymentNotification'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant_order_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'order_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['walletone']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BlogMainPage'
        db.create_table(u'blog_blogmainpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page_title', self.gf('django.db.models.fields.TextField')()),
            ('page_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('page_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'blog', ['BlogMainPage'])

        # Adding model 'BlogTag'
        db.create_table(u'blog_blogtag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'blog', ['BlogTag'])

        # Adding model 'BlogItem'
        db.create_table(u'blog_blogitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page_title', self.gf('django.db.models.fields.TextField')()),
            ('page_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('page_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('create_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, db_index=True)),
            ('preview_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('detail_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('content', self.gf('redactor.fields.RedactorField')()),
        ))
        db.send_create_signal(u'blog', ['BlogItem'])

        # Adding M2M table for field tags on 'BlogItem'
        m2m_table_name = db.shorten_name(u'blog_blogitem_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blogitem', models.ForeignKey(orm[u'blog.blogitem'], null=False)),
            ('blogtag', models.ForeignKey(orm[u'blog.blogtag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blogitem_id', 'blogtag_id'])


    def backwards(self, orm):
        # Deleting model 'BlogMainPage'
        db.delete_table(u'blog_blogmainpage')

        # Deleting model 'BlogTag'
        db.delete_table(u'blog_blogtag')

        # Deleting model 'BlogItem'
        db.delete_table(u'blog_blogitem')

        # Removing M2M table for field tags on 'BlogItem'
        db.delete_table(db.shorten_name(u'blog_blogitem_tags'))


    models = {
        u'blog.blogitem': {
            'Meta': {'object_name': 'BlogItem'},
            'content': ('redactor.fields.RedactorField', [], {}),
            'create_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'db_index': 'True'}),
            'detail_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page_title': ('django.db.models.fields.TextField', [], {}),
            'preview_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blog.BlogTag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'blog.blogmainpage': {
            'Meta': {'object_name': 'BlogMainPage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page_title': ('django.db.models.fields.TextField', [], {})
        },
        u'blog.blogtag': {
            'Meta': {'object_name': 'BlogTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['blog']
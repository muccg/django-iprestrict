# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IPGroup'
        db.create_table('iprestrict_ipgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('iprestrict', ['IPGroup'])

        # Adding model 'IPRange'
        db.create_table('iprestrict_iprange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iprestrict.IPGroup'])),
            ('first_ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('cidr_prefix_length', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('last_ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
        ))
        db.send_create_signal('iprestrict', ['IPRange'])

        # Adding model 'Rule'
        db.create_table('iprestrict_rule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_pattern', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('ip_group', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['iprestrict.IPGroup'])),
            ('action', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('iprestrict', ['Rule'])

        # Adding model 'ReloadRulesRequest'
        db.create_table('iprestrict_reloadrulesrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('iprestrict', ['ReloadRulesRequest'])


    def backwards(self, orm):
        
        # Deleting model 'IPGroup'
        db.delete_table('iprestrict_ipgroup')

        # Deleting model 'IPRange'
        db.delete_table('iprestrict_iprange')

        # Deleting model 'Rule'
        db.delete_table('iprestrict_rule')

        # Deleting model 'ReloadRulesRequest'
        db.delete_table('iprestrict_reloadrulesrequest')


    models = {
        'iprestrict.ipgroup': {
            'Meta': {'object_name': 'IPGroup'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'iprestrict.iprange': {
            'Meta': {'object_name': 'IPRange'},
            'cidr_prefix_length': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iprestrict.IPGroup']"}),
            'last_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'})
        },
        'iprestrict.reloadrulesrequest': {
            'Meta': {'object_name': 'ReloadRulesRequest'},
            'at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'iprestrict.rule': {
            'Meta': {'ordering': "['rank', 'id']", 'object_name': 'Rule'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_group': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['iprestrict.IPGroup']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'url_pattern': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['iprestrict']

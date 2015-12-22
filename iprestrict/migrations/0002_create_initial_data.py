# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        # Default IP Groups: ALL and localhost
        all_group = orm.IPGroup.objects.create(
            name='ALL', description="Matches all IP Addresses")
        localhost_group = orm.IPGroup.objects.create(
            name='localhost', description="IP Address of localhost")

        # IP ranges defining ALL and localhost for ipv4 and ipv6
        orm.IPRange.objects.create(ip_group=all_group,
            first_ip = '0.0.0.0', last_ip = '255.255.255.255')
        orm.IPRange.objects.create(ip_group=all_group,
            first_ip = '0:0:0:0:0:0:0:0',
            last_ip = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')

        orm.IPRange.objects.create(ip_group=localhost_group,
            first_ip = '127.0.0.1')
        orm.IPRange.objects.create(ip_group=all_group,
            first_ip = '::1')

        # Default rules: Allow all for localhost and Deny everything else

        orm.Rule.objects.create(ip_group=localhost_group,
            action = 'A', url_pattern = 'ALL', rank=65535)
        orm.Rule.objects.create(ip_group=all_group,
            action = 'A', url_pattern = 'ALL', rank=65536)


    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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

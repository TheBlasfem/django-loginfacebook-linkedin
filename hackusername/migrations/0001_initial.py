# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MyUser'
        db.create_table('cn_my_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('commercial_name', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('business_name', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('ruc', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('web', self.gf('django.db.models.fields.URLField')(max_length=150, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'hackusername', ['MyUser'])

        # Adding M2M table for field groups on 'MyUser'
        m2m_table_name = db.shorten_name('cn_my_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myuser', models.ForeignKey(orm[u'hackusername.myuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['myuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'MyUser'
        m2m_table_name = db.shorten_name('cn_my_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myuser', models.ForeignKey(orm[u'hackusername.myuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['myuser_id', 'permission_id'])

        # Adding model 'Role'
        db.create_table('cn_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cod', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'hackusername', ['Role'])

        # Adding model 'RoleUser'
        db.create_table('cn_role_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hackusername.MyUser'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hackusername.Role'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Event'])),
        ))
        db.send_create_signal(u'hackusername', ['RoleUser'])

        # Adding model 'Permission'
        db.create_table('cn_permission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cod', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'hackusername', ['Permission'])

        # Adding model 'RolePermission'
        db.create_table('cn_role_permission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hackusername.Permission'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hackusername.Role'])),
        ))
        db.send_create_signal(u'hackusername', ['RolePermission'])


    def backwards(self, orm):
        # Deleting model 'MyUser'
        db.delete_table('cn_my_user')

        # Removing M2M table for field groups on 'MyUser'
        db.delete_table(db.shorten_name('cn_my_user_groups'))

        # Removing M2M table for field user_permissions on 'MyUser'
        db.delete_table(db.shorten_name('cn_my_user_user_permissions'))

        # Deleting model 'Role'
        db.delete_table('cn_role')

        # Deleting model 'RoleUser'
        db.delete_table('cn_role_user')

        # Deleting model 'Permission'
        db.delete_table('cn_permission')

        # Deleting model 'RolePermission'
        db.delete_table('cn_role_permission')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hackusername.myuser': {
            'Meta': {'object_name': 'MyUser', 'db_table': "'cn_my_user'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'commercial_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'ruc': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        u'hackusername.permission': {
            'Meta': {'object_name': 'Permission', 'db_table': "'cn_permission'"},
            'cod': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'hackusername.role': {
            'Meta': {'object_name': 'Role', 'db_table': "'cn_role'"},
            'cod': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'hackusername.rolepermission': {
            'Meta': {'object_name': 'RolePermission', 'db_table': "'cn_role_permission'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hackusername.Permission']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hackusername.Role']"})
        },
        u'hackusername.roleuser': {
            'Meta': {'object_name': 'RoleUser', 'db_table': "'cn_role_user'"},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hackusername.Role']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hackusername.MyUser']"})
        },
        u'registration.event': {
            'Meta': {'object_name': 'Event', 'db_table': "'cn_event'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['hackusername']
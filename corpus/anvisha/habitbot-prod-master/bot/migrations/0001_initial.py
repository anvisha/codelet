# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Participant'
        db.create_table('bot_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='participant', unique=True, to=orm['auth.User'])),
            ('twitterid', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('oauth_token', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('oauth_secret', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created_acct', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('bot', ['Participant'])

        # Adding model 'Goal'
        db.create_table('bot_goal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='goals', to=orm['bot.Participant'])),
            ('goalname', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('hashtag', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('punishmsg', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('rewardmsg', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('donttweet', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('firsttweet', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('punishtime', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('rewardtime', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('rewardlength', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('is_paused', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('is_done', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal('bot', ['Goal'])

        # Adding model 'Pageview'
        db.create_table('bot_pageview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pageviews', to=orm['bot.Participant'])),
            ('page_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pageviews', null=True, to=orm['bot.Goal'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('bot', ['Pageview'])

        # Adding model 'Update'
        db.create_table('bot_update', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updates', to=orm['bot.Participant'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updates', to=orm['bot.Goal'])),
            ('goalname', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('hashtag', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firsttweet', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('punishmsg', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('rewardmsg', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('donttweet', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('is_paused', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_done', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('bot', ['Update'])

        # Adding model 'Day'
        db.create_table('bot_day', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='days', to=orm['bot.Participant'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='days', to=orm['bot.Goal'])),
            ('timestamp', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('is_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tweet', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('tweet_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('tweet_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('bot', ['Day'])

        # Adding model 'Messages'
        db.create_table('bot_messages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message_type', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages', to=orm['bot.Participant'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages', to=orm['bot.Goal'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal('bot', ['Messages'])


    def backwards(self, orm):
        # Deleting model 'Participant'
        db.delete_table('bot_participant')

        # Deleting model 'Goal'
        db.delete_table('bot_goal')

        # Deleting model 'Pageview'
        db.delete_table('bot_pageview')

        # Deleting model 'Update'
        db.delete_table('bot_update')

        # Deleting model 'Day'
        db.delete_table('bot_day')

        # Deleting model 'Messages'
        db.delete_table('bot_messages')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bot.day': {
            'Meta': {'object_name': 'Day'},
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'days'", 'to': "orm['bot.Goal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'days'", 'to': "orm['bot.Participant']"}),
            'timestamp': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tweet': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tweet_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tweet_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'bot.goal': {
            'Meta': {'object_name': 'Goal'},
            'donttweet': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'firsttweet': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'goalname': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'hashtag': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'is_paused': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goals'", 'to': "orm['bot.Participant']"}),
            'punishmsg': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'punishtime': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'rewardlength': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rewardmsg': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'rewardtime': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'bot.messages': {
            'Meta': {'object_name': 'Messages'},
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': "orm['bot.Goal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': "orm['bot.Participant']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'bot.pageview': {
            'Meta': {'object_name': 'Pageview'},
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pageviews'", 'null': 'True', 'to': "orm['bot.Goal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pageviews'", 'to': "orm['bot.Participant']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'bot.participant': {
            'Meta': {'object_name': 'Participant'},
            'created_acct': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oauth_secret': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'twitterid': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'participant'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'bot.update': {
            'Meta': {'object_name': 'Update'},
            'donttweet': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'firsttweet': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updates'", 'to': "orm['bot.Goal']"}),
            'goalname': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'hashtag': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_paused': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updates'", 'to': "orm['bot.Participant']"}),
            'punishmsg': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'rewardmsg': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bot']
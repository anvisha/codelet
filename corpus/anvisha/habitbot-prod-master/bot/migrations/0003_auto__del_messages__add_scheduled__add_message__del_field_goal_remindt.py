# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Messages'
        db.delete_table('bot_messages')

        # Adding model 'Scheduled'
        db.create_table('bot_scheduled', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message_type', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sched_participant', to=orm['bot.Participant'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sched_goal', to=orm['bot.Goal'])),
            ('day_of_week', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('time_of_day', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('bot', ['Scheduled'])

        # Adding model 'Message'
        db.create_table('bot_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message_state', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='msg_participant', to=orm['bot.Participant'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='msg_goal', to=orm['bot.Goal'])),
            ('time_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_sent', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('message_sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender', to=orm['bot.Participant'])),
            ('reply_to_id', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('num_tries', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('message_text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('scheduled_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scheduledby', to=orm['bot.Scheduled'])),
        ))
        db.send_create_signal('bot', ['Message'])

        # Deleting field 'Goal.remindtime'
        db.delete_column('bot_goal', 'remindtime')

        # Deleting field 'Goal.rewardtime'
        db.delete_column('bot_goal', 'rewardtime')

        # Deleting field 'Goal.is_done'
        db.delete_column('bot_goal', 'is_done')

        # Deleting field 'Goal.punishtime'
        db.delete_column('bot_goal', 'punishtime')

        # Deleting field 'Goal.rewardlength'
        db.delete_column('bot_goal', 'rewardlength')

        # Adding field 'Goal.remind_tod'
        db.add_column('bot_goal', 'remind_tod',
                      self.gf('django.db.models.fields.TimeField')(null=True),
                      keep_default=False)

        # Adding field 'Goal.remind_dow'
        db.add_column('bot_goal', 'remind_dow',
                      self.gf('django.db.models.fields.CharField')(default='*', max_length=1),
                      keep_default=False)

        # Adding field 'Goal.punish_tod'
        db.add_column('bot_goal', 'punish_tod',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.time(23, 59)),
                      keep_default=False)

        # Adding field 'Goal.reward_tod'
        db.add_column('bot_goal', 'reward_tod',
                      self.gf('django.db.models.fields.TimeField')(null=True),
                      keep_default=False)

        # Adding field 'Goal.reward_dow'
        db.add_column('bot_goal', 'reward_dow',
                      self.gf('django.db.models.fields.CharField')(default='6', max_length=1),
                      keep_default=False)

        # Adding field 'Goal.is_done_today'
        db.add_column('bot_goal', 'is_done_today',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Messages'
        db.create_table('bot_messages', (
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages', to=orm['bot.Participant'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages', to=orm['bot.Goal'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('message_type', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('bot', ['Messages'])

        # Deleting model 'Scheduled'
        db.delete_table('bot_scheduled')

        # Deleting model 'Message'
        db.delete_table('bot_message')

        # Adding field 'Goal.remindtime'
        db.add_column('bot_goal', 'remindtime',
                      self.gf('django.db.models.fields.TimeField')(null=True),
                      keep_default=False)

        # Adding field 'Goal.rewardtime'
        db.add_column('bot_goal', 'rewardtime',
                      self.gf('django.db.models.fields.TimeField')(null=True),
                      keep_default=False)

        # Adding field 'Goal.is_done'
        db.add_column('bot_goal', 'is_done',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Goal.punishtime'
        db.add_column('bot_goal', 'punishtime',
                      self.gf('django.db.models.fields.TimeField')(null=True),
                      keep_default=False)

        # Adding field 'Goal.rewardlength'
        db.add_column('bot_goal', 'rewardlength',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Deleting field 'Goal.remind_tod'
        db.delete_column('bot_goal', 'remind_tod')

        # Deleting field 'Goal.remind_dow'
        db.delete_column('bot_goal', 'remind_dow')

        # Deleting field 'Goal.punish_tod'
        db.delete_column('bot_goal', 'punish_tod')

        # Deleting field 'Goal.reward_tod'
        db.delete_column('bot_goal', 'reward_tod')

        # Deleting field 'Goal.reward_dow'
        db.delete_column('bot_goal', 'reward_dow')

        # Deleting field 'Goal.is_done_today'
        db.delete_column('bot_goal', 'is_done_today')


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
            'is_done_today': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'is_paused': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goals'", 'to': "orm['bot.Participant']"}),
            'punish_tod': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(23, 59)'}),
            'punishmsg': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'remind_dow': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '1'}),
            'remind_tod': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'remindmsg': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True'}),
            'reward_dow': ('django.db.models.fields.CharField', [], {'default': "'6'", 'max_length': '1'}),
            'reward_tod': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'rewardmsg': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'bot.message': {
            'Meta': {'object_name': 'Message'},
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'msg_goal'", 'to': "orm['bot.Goal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'to': "orm['bot.Participant']"}),
            'message_state': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'message_text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'num_tries': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'msg_participant'", 'to': "orm['bot.Participant']"}),
            'reply_to_id': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'scheduled_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scheduledby'", 'to': "orm['bot.Scheduled']"}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_sent': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        'bot.scheduled': {
            'Meta': {'object_name': 'Scheduled'},
            'day_of_week': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sched_goal'", 'to': "orm['bot.Goal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sched_participant'", 'to': "orm['bot.Participant']"}),
            'time_of_day': ('django.db.models.fields.TimeField', [], {})
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
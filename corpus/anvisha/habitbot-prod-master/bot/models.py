from django.db import models
from django import forms
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Participant(models.Model):
    user         = models.OneToOneField(User, related_name="participant")
    twitterid    = models.CharField(max_length=140)
    oauth_token  = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)
    created_acct = models.DateTimeField(auto_now_add=True)
    invited      = models.BooleanField(default=False)
    def __unicode__(self):
        return self.twitterid

class InviteForm(forms.Form):
    twitterid    = forms.CharField(max_length=140) 
    invitecode   = forms.CharField(max_length=140)

class ContactForm(forms.Form):
    partname     = forms.CharField(max_length=140)
    twitterid    = forms.CharField(max_length=140)
    email        = forms.EmailField()
    habit        = forms.CharField(max_length=140)

class Invite(models.Model):
    partname     = models.CharField(max_length=140)
    twitterid    = models.CharField(max_length=140)
    email        = models.CharField(max_length=140)
    habit        = models.CharField(max_length=140)
    inviteused   = models.NullBooleanField(default=False)
    invitecode   = models.CharField(max_length=140, null=True)

class Goal(models.Model):
    DAY_OF_WEEK = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
        ('*', 'Every day'),
    )
    participant  = models.ForeignKey(Participant, related_name="goals")
    goalname     = models.CharField(max_length=140)
    hashtag      = models.CharField(max_length=50)
    shortname    = models.CharField(max_length=40, null=True)
    # reminders
    remindmsg    = models.CharField(max_length=140, null=True)
    remind_tod   = models.TimeField(null=True)
    remind_dow   = models.CharField(max_length = 1, choices = DAY_OF_WEEK, default="*")
    # punishments
    punishmsg    = models.CharField(max_length=140)
    punish_tod   = models.TimeField(null=False, default=datetime.time(23,59))
    punish_dow   = models.CharField(max_length=1, choices=DAY_OF_WEEK, default="*")
    # rewards
    rewardmsg    = models.CharField(max_length=140)
    reward_tod   = models.TimeField(null=True)
    reward_dow   = models.CharField(max_length=1, choices=DAY_OF_WEEK, default="6", null=True)
    # bool used for what?
    donttweet    = models.NullBooleanField(default=False)
    # their first tweet
    firsttweet   = models.CharField(max_length=140)
    # is this paused for now?
    is_paused    = models.NullBooleanField(default=False)
    # is this done today?
    is_done_today= models.NullBooleanField(default=False)
    #  last_edit    = models.DateTimeField(auto_now=True)
    friend1      = models.CharField(max_length=140, null=True)
    friend2      = models.CharField(max_length=140, null=True)
    friend3      = models.CharField(max_length=140, null=True)
    friend4      = models.CharField(max_length=140, null=True)
    friend5      = models.CharField(max_length=140, null=True)
    PING_CONDS = (
        ('never', "Never ping anyone"),
        ('start', "When the goal is created"),
        ('failure', "When the user fails several times"),
        ('success', "When the user succeeds several times"),
    )
    ping_cond    = models.CharField(max_length=7, choices=PING_CONDS, default="never")
    success_streak=models.IntegerField(default=0)
    failure_streak=models.IntegerField(default=0)
    def __unicode__(self):
        return self.goalname

class Pageview(models.Model):
    participant  = models.ForeignKey(Participant, related_name="pageviews")
    # this is the url path - is page_name + goal necessary?
    page_name    = models.CharField(max_length=100)
    goal         = models.ForeignKey(Goal, related_name="pageviews", null=True, blank=True)
    timestamp    = models.DateTimeField(auto_now_add=True)

class Update(models.Model):
    ## this is just broken. diverges from Goal model too quickly.
    participant  = models.ForeignKey(Participant, related_name="updates")
    goal         = models.ForeignKey(Goal, related_name="updates")
    goalname     = models.CharField(max_length=140, blank=True)
    hashtag      = models.CharField(max_length=50)
    firsttweet   = models.CharField(max_length=140)
    punishmsg    = models.CharField(max_length=140, blank=True)
    rewardmsg    = models.CharField(max_length=140, blank=True)
    donttweet    = models.NullBooleanField(default=False)
    is_paused    = models.NullBooleanField(blank=True)
    is_done_today= models.NullBooleanField(blank=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
       return str(self.goal)

class Day(models.Model):
    participant  = models.ForeignKey(Participant, related_name="days")
    goal         = models.ForeignKey(Goal, related_name="days")
    timestamp    = models.DateField(auto_now_add=True)
    is_done_today= models.BooleanField(default=False)
    tweet        = models.CharField(max_length=140,blank=False)
    tweet_id     = models.IntegerField(blank=False, db_index=True)
    tweet_time   = models.DateTimeField(blank=False)
    def __unicode__(self):
        return self.tweet

class Scheduled(models.Model):
    # this is the queue for messages.
# this keeps track of tasks that happen for each user.
    MSG_TYPE = (
        ('remind', 'reminder_msg.py'),
        ('punish', 'punish_msg.py'),
        ('reward', 'reward_msg.py'),
        )
    DAY_OF_WEEK = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
        ('*', 'Every day'),
    )
    message_type  = models.CharField(max_length=6, choices=MSG_TYPE)
    participant   = models.ForeignKey(Participant, related_name="sched_participant")
    goal          = models.ForeignKey(Goal, related_name="sched_goal")
    day_of_week   = models.CharField(max_length=1, choices=DAY_OF_WEEK, null=False)
    time_of_day   = models.TimeField(null=False)
# We'll store a time with a buffer (5 mins), which will eventually be used before sending punishment messages, so people have a slight grace period. Not used currently.
    time_w_buffer = models.TimeField(null=True)
    def __unicode__(self):
        return self.message_type

class Message(models.Model):
# this keeps track of all of the messages we send. send_msg iterates through these and checks for pending tweets and tries to send them.
    MSG_STATE = (
        ('PENDING', 'pending'),
        ('SENT', 'sent'),
        ('FAILED', 'failed'),
        )
    message_state = models.CharField(max_length=6, choices=MSG_STATE)
    participant   = models.ForeignKey(Participant, related_name="msg_participant")
    goal          = models.ForeignKey(Goal, related_name="msg_goal")
    time_added    = models.DateTimeField(auto_now_add=True)
    time_sent     = models.DateTimeField(auto_now=True)
    message_sender= models.ForeignKey(Participant, related_name="sender")
    reply_to_id   = models.CharField(max_length=140, blank=True)
    num_tries     = models.IntegerField(null=False, default=0)
    message_text  = models.CharField(max_length=140, null=False)
    scheduled_by  = models.ForeignKey(Scheduled, related_name="scheduledby")
    def __unicode__(self):
        return self.message_state

class TieStrength(models.Model):
    participant   = models.ForeignKey(Participant, related_name='ts_part')
    goal          = models.ForeignKey(Goal, related_name='ts_goal')
    friend_id     = models.CharField(max_length=140, null=True) #twitter id of friend
    


    # this should store completed tie strength number
    # as well as each of the numbers that go into the model, probably. at least for now.


class OneOff(models.Model):
# this keeps track of states for different things
    # this is the name for filtering
    name          = models.CharField(max_length=10)
    # last time the Scheduled cron job ran
    scheduled_ran = models.DateTimeField(auto_now=True)
    # last tweet id that we pulled
    tweet_since   = models.IntegerField(blank=False)
    def __unicode__(self):
        string1 = "Scheduled_ran is "+ str(self.scheduled_ran)
        string_sp= ", "
        string2 = "Tweet since is" + str(self.tweet_since)
        return string1+string_sp+string2

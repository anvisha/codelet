from django.core.management import setup_environ
# this import lets us use ORs in db queries
from django.db.models import Q
from habitbot import settings
import tweepy
import random
import datetime
import remind
import reward
import punish

setup_environ(settings)

from bot.models import Participant, Goal, Scheduled, Message, OneOff 

# this is what runs when the cron job is called

class Msg_Queue(object):
    def __init__(self):

        # get the current time
        now = datetime.datetime.now()
# get this from now instead
        today = datetime.date.weekday()

        # these are all of the messages that are in the queue leading up to now
        # should also filter for day, and last time the cron job ran...
        schedule_queue = (Scheduled.objects.                        #filtering Scheduled for...
                        filter(time_w_buffer__lte=now).             #time before now 
                        filter(time_w_buffer___gte=                 #but after the last job ran
                        OneOff.objects.get(name='main').scheduled_ran).
                        filter(Q(day_of_week=today)                 #on today
                        |Q(day_of_week='*'))                        #incl. every day
                        )

        # list that holds the things to return, used purely for testing
        ret_list=[]

        # iterate through it
        for item in schedule_queue:
            if item.message_type == "remind":
                ret_list.append(str(remind.remind_sender(item)))
            elif item.message_type == "punish":
                ret_list.append(str(punish.punish_sender(item)))
            elif item.message_type == "reward":
                ret_list.append(str(reward.reward_sender(item)))
            else:
                print "shouldn't have gotten here"

            # call get_replies.py or whatever using the appropriate info
# call the message sender here right away to give things a shot; we'll also be checking a minute later and subsequently anyway, but good to get it immediately
        return ret_list.sort()

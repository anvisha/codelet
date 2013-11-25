'''
Every message_type handler should:
1. check accuracy. compare to goal object, and update Scheduled model if necessary.
2. check Message table for existing scheduled_by && PENDING
3. make the new tweet text and store it in message_text (this should include @mentions)
4. message_sender depends on the handler; punish & reward is participant, remind (and otherwise) is habitbot
5. add it to the table
'''


from django.core.management import setup_environ
from django.utils.timezone import utc
from habitbot import settings
import tweepy
import random
from datetime import datetime
from datetime import timedelta

setup_environ(settings)

from bot.models import Participant, Goal, Day, Message, Scheduled

def punish_sender(scheduled_item):

    #check to see if message still accurate
    stored_tod = scheduled_item.goal.punish_tod
    stored_dow = scheduled_item.goal.punish_dow
    # if it's not, save the new thing and return
    if (stored_tod != scheduled_item.time_of_day) or (stored_dow != scheduled_item.day_of_week):
        scheduled_item.time_of_day = stored_tod
        scheduled_item.day_of_week = stored_dow
        scheduled_item.save()
        return
    
    #check to see if message is pending in queue. If not, add.
    message_obj = Message.objects.get(id=scheduled_item.id)
    if message_obj == None or message_obj.message_state != 'PENDING':
        created_msg = Message.objects.create(message_state = 'PENDING',
                               participant = scheduled_item.participant, 
                               goal = scheduled_item.goal,
                               message_sender = participant,
                               num_tries = 0,
                               message_text = scheduled_item.goal.punishmsg,
                               scheduled_by = scheduled_item.id)
    return str(created_msg+' punish')

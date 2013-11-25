"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test bot".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
from bot.models import *
from authentication.models import *
from django.contrib.auth.models import User
import datetime
import time
from message_queue import Msg_Queue

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        print "testing addition"
        self.assertEqual(1 + 1, 2)

class CreateParticipant(TestCase):
    def test_participant_creation(self):
        """
        trying to write a test
        """

        # create a user 
        userobj = User.objects.create_user("kp_party_bus")
        participant = Participant.objects.create(user=userobj, 
                                twitterid="kp_party_bus", 
                                oauth_token="545459845-YGcjJMjp2ejvdVyyMr28MtU0XpGaF9PWEfZCwSd5", 
                                oauth_secret="fNjSBVZBWLxhkPu2mVCHPQsAVf4OR0Mybfd1lQLg"
                                )

        self.assertEqual(participant.twitterid, "kp_party_bus")

class MessageQueueTest(TestCase):
    def test_filtering(self):
        """
        trying to write a test
        """
        OneOff.objects.create(name='main', tweet_since=0)
        # now sleep for a bit so that this is  minutes ago.
        time.sleep(1*6)


        # some time stuff i need
        currently=datetime.datetime.now()

        temp_seconds = currently.time().second - 30
        temp_minutes = currently.time().minute
        if temp_seconds < 0 :
            temp_minutes = temp_minutes - 1
            temp_seconds = temp_seconds + 60

        previously = datetime.datetime(year=currently.year, 
                                   month=currently.month, 
                                   day=currently.day, 
                                   hour=currently.hour, 
                                   minute=temp_minutes, 
                                   second=temp_seconds
                                   ) # ignore anything sub seconds. we don't need that precision

        today_dow=datetime.date.weekday(currently)

        half_a_minute_ago=previously.time()

        # create a user 
        userobj = User.objects.create_user("kp_party_bus")
        participant = Participant.objects.create(user=userobj, 
                                twitterid="kp_party_bus", 
                                oauth_token="545459845-YGcjJMjp2ejvdVyyMr28MtU0XpGaF9PWEfZCwSd5", 
                                oauth_secret="fNjSBVZBWLxhkPu2mVCHPQsAVf4OR0Mybfd1lQLg"
                                )
        # create a goal
        goal1 = Goal.objects.create(participant=participant,
                                    goalname="goal1",
                                    hashtag="#goal1",
                                    shortname="goal1",
                                    remindmsg="remind goal1",
                                    remind_tod=half_a_minute_ago,
                                    remind_dow=today_dow,
                                    punishmsg="remind goal1",
                                    punish_tod=half_a_minute_ago,
                                    punish_dow=today_dow,
                                    rewardmsg="remind goal1",
                                    reward_tod=half_a_minute_ago,
                                    reward_dow=today_dow,
                                    donttweet=False,
                                    firsttweet="some tweet",
                                    is_paused=False,
                                    is_done_today=False
                                    )


        '''
        What this test should do:
        1. put some fake messages in the message queue
        2. put a fake last cron time in the OneOff table
        3. run the message thing and see if some objects get pulled up
        4. change time and get the other items?
        '''
        

        #start by testing normal.

        # list to compare
        compare_list = []

        # Now last cron time is one minute ago
        Scheduled.objects.create(message_type='remind',
                                 participant=participant,
                                 goal=goal1,
                                 day_of_week=today_dow,
                                 time_of_day=half_a_minute_ago,
                                 time_w_buffer=half_a_minute_ago
                                 )
        # create an item in the list to compare to output from msg queue
        compare_list.append('pending remind')
        
        Scheduled.objects.create(message_type='reward',
                                 participant=participant,
                                 goal=goal1,
                                 day_of_week="*",
                                 time_of_day=half_a_minute_ago,
                                 time_w_buffer=half_a_minute_ago
                                 )
        
        # create an item in the list to compare to output from msg queue
        compare_list.append('pending reward')

        Scheduled.objects.create(message_type='punish',
                                 participant=participant,
                                 goal=goal1,
                                 day_of_week=today_dow,
                                 time_of_day=half_a_minute_ago,
                                 time_w_buffer=half_a_minute_ago
                                 )
        
        # create an item in the list to compare to output from msg queue
        compare_list.append('pending punish')

        # now run the queue parser
        returned_list = Msg_Queue()

        #finall assert that compared and returned are equal
        assertEqual(returned_list, compared_list)

from django.core.management import setup_environ
from habitbot import settings
import tweepy
import random

setup_environ(settings)

from bot.models import Participant, Goal, Day, Message

# this uses the consumer key & secret for habitbot
auth = tweepy.OAuthHandler("DYe0C4rw7VlDyRanFRrj3g", "9U74ene1QruXZIMbKAnSBbBRbfJ4YNkQCQvbrkGs")

twitterbot = Participant.objects.get(twitterid="habitbot")
auth.set_access_token(twitterbot.oauth_token, twitterbot.oauth_secret)
api = tweepy.API(auth)

# first we get all of the replies since the last time
try:
    since = Day.objects.order_by('-tweet_id')[0].tweet_id
    mentions = api.mentions_timeline(since_id=since)
except:
    mentions = api.mentions_timeline()

# then we iterate through all of those mentions
for mention in mentions :
    participant = Participant.objects.get(twitterid=mention.user.screen_name)
    # this only looks at the first goal
    goal = participant.goals.all()[0]
    day = Day.objects.create(participant=participant,
                             goal=goal,
                             tweet=mention.text,
			# this saves a naive datetime, when we could save one with timezone info
                             tweet_time=mention.created_at,
                             tweet_id=mention.id,
                             is_done_today=True)
    goal.is_done_today = day.is_done_today
    goal.save()
    thanks_string = "@"+participant.twitterid+" got it! thanks, "+participant.twitterid+"! "+r
# add to the messages pool, where it will get called by send_msg
# is it okay that we don't have a scheduled_by here?
    message = Message.objects.create(message_state='PENDING', 
                                     participant=participant, 
                                     goal=goal, 
                                     message_sender=twitterbot, 
                                     reply_to_id=mention.id, 
                                     num_tries=0, 
                                     message_text=thanks_string)

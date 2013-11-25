from django.core.management import setup_environ
from habitbot import settings
from bot.models import Participant, Goal
import tweepy
import random

setup_environ(settings)

def message_sender(participant, text):
    # this uses the consumer key & secret for habitbot
    auth = tweepy.OAuthHandler("DYe0C4rw7VlDyRanFRrj3g", "9U74ene1QruXZIMbKAnSBbBRbfJ4YNkQCQvbrkGs")

    auth.set_access_token
    auth.set_access_token(participant.oauth_token, participant.oauth_secret)
    api = tweepy.API(auth)

    r = str(int(100*random.random()))
    try:
        api.update_status(text)
    except:
        api.update_status(text + " " +r)
    print participant.twitterid + " " + text + "\n"




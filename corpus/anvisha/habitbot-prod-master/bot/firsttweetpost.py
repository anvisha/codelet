from django.core.management import setup_environ
from habitbot import settings
import tweepy
import random

setup_environ(settings)

from bot.models import * 

# this uses the consumer key & secret for habitbot
auth = tweepy.OAuthHandler("DYe0C4rw7VlDyRanFRrj3g", "9U74ene1QruXZIMbKAnSBbBRbfJ4YNkQCQvbrkGs")

auth.set_access_token


def postfirsttweet(participant, goal):
    firsttweet = goal.firsttweet
    print "first tweet in postfirsttweet : ", firsttweet
    auth.set_access_token(participant.oauth_token, participant.oauth_secret)
    api = tweepy.API(auth)
    api.update_status(firsttweet)

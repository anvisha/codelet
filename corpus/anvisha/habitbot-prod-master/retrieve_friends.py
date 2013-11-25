from django.core.management import setup_environ
from django.utils.timezone import utc
from habitbot import settings
import tweepy

setup_environ(settings)

from bot.models import Participant

#returns list of strings of friends' twitter IDs.
def get_friends(twitter_id):

    #.screen_name , .name and .profile_image_url

	#authorization
    auth = tweepy.OAuthHandler("DYe0C4rw7VlDyRanFRrj3g", "9U74ene1QruXZIMbKAnSBbBRbfJ4YNkQCQvbrkGs")
    #auth.set_access_token

    participant = Participant.objects.get(twitterid = twitter_id)

    auth.set_access_token(participant.oauth_token, participant.oauth_secret)
    api = tweepy.API(auth)

    #get followees
    followees = api.friends() #list of ids of people the user is following
    #print [(x.screen_name, x) for x in followees]
    followees_handles = [x.screen_name for x in followees]

    #get followers
    followers = api.followers()
    followers_handles = [x.screen_name for x in followers]


    #get "friends"-- bidirectional followers
    friends_handles = list(set(followees_handles)&set(followers_handles))
    print friends_handles
    friends = []
    for user in followees:
        if user.screen_name in friends_handles:
            friends.append(user)

    #friends_handles = [str(api.get_user(person).screen_name) for person in friends]
    #friends_information = [{"screen_name": friend.screen_name, "name": friend.name, "img": friend.profile_image_url} for friend in friends]
    return friends
    

    #return ["hi", "this", "is", "anvisha"]

#>>> import tweepy
#>>> auth = tweepy.OAuthHandler("DYe0C4rw7VlDyRanFRrj3g", "9U74ene1QruXZIMbKAnSBbBRbfJ4YNkQCQvbrkGs")
#>>> from bot.models import *
#>>> participant = Participant.objects.get(twitterid = 'habitbot')
#>>> auth.set_access_token(participant.oauth_token, participant.oauth_secret)
#>>> api = tweepy.API(auth)
#>>> followees = api.friends_ids()
#>>> followers = api.followers_ids()
#>>> friends = list(set(followees)&set(followers))
#>>> friends_obj = api.lookup_users(user_ids=friends)
#>>> for person in friends_obj:
#...     person.screen_name

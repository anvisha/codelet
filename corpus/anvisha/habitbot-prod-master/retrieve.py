from django.core.management import setup_environ
from django.utils.timezone import utc
from habitbot import settings
import tweepy

setup_environ(settings)

from bot.models import Participant

def get_params(twitter_id):
    auth = tweepy.OAuthHandler("DYe0C4rw7VlDyRanFRrj3g", "9U74ene1QruXZIMbKAnSBbBRbfJ4YNkQCQvbrkGs")
    auth.set_access_token

    participant = Participant.objects.get(twitterid = twitter_id)

    auth.set_access_token(participant.oauth_token, participant.oauth_secret)
    api = tweepy.API(auth)

    friends = api.friends_ids() #list of ids of people the user is following

    friends = api.friends_ids() #list of ids of people the user is following
    friend_values ={}

    '''

    for friend in friends:
        friend_id = api.get_user(friend).screen_name
        friend_values[friend_id] = ["",""] #[user->friend words, ]

    tweets = api.user_timeline()

    for tweet in tweets:
        if tweet.in_reply_to_screen_name in friend_values:
'''

    reply_words_out = {}

    

    #for friend in friends:

    #friend_id = api.get_user(friend).screen_name
    friend_id = "anvishapai"
    text = ""
    user_to_friend = "from%3A"+twitter_id+"+AND+to%3A"+friend_id
    print user_to_friend
    result_tweets = api.search("from%3A"+twitter_id)
    print result_tweets, "result tweets "
    print len(result_tweets) ,"number of tweets"
    for tweet in result_tweets:
        print tweet
        text+= tweet.text
    reply_words_out[friend_id] = text


        #q="to%3A"
        #at mentions
        #q= "%40"+


    '''
    twitter_info = {
                    'friend_twitter_id': twitter_id,
                    ''

    }
    
    
    recent_status = api.user_timeline()
    for i in recent_status:
        print i.text
    

    first_foll = api.followers()[0]
    print first_foll.screen_name
    '''

    return reply_words_out
    

    

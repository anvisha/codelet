from django.core.management import setup_environ
from django.utils.timezone import utc
from habitbot import settings
import tweepy

setup_environ(settings)

from bot.models import Participant

params_per_friend = { 'screen_name': '',
                    'last_comm':None, 
                    'first_comm':None, 
                    'reply_words':0, 
                    'reply_intimacy_words':0,
                    'initiated':0,
                    'link_sharing':0,
                    'follower_count':0,
                    'direct_messages':0}


#param: string tweet_text, text of tweet
#returns: tuple of (tweet_length, intimacy_count) where tweet_length = number of words, intimacy_count = number of intimacy words
def process_tweet(tweet):

    #print "parsing", tweet_text

    #number of links in tweet
    links = len(tweet.entities['urls'])

    #split tweet into words
    tweet_words = tweet.text.split( )

    print tweet_words
    tweet_length = len(tweet_words)

    #count intimacy words
    intimacy_words = ['love', 'what', 'hey']
    intimacy_count = 0

    for word in tweet_words:
        if word in intimacy_words:
            intimacy_count += 1

    return (tweet_length, intimacy_count, links)


#param: api object, params dictionary
#returns: updated params dictionary
#traverses all available user statuses, retrieving information on @reply statuses and updating params
def process_statuses(api, params):

    #pulls up statuses. "entities" set to true so we can closely examine status objects
    statuses = api.user_timeline(count=1000, include_entities=True)
    i=0 #variable to keep track of statuses traversed

    
    for tweet in statuses:
        i += 1
        
        friend_mentions = tweet.entities['user_mentions']

        if friend_mentions!=[]:
            
            (tweet_length, intimacy_count, links) = process_tweet(tweet)
            reply_to = tweet.in_reply_to_user_id

            for friend in friend_mentions:

                friend_id = friend['id']

                params[friend_id]['reply_words'] += tweet_length
                params[friend_id]['reply_intimacy_words'] += intimacy_count
                params[friend_id]['link_sharing'] += links


                #who was this conversation initiated by
                if reply_to != friend_id:
                    params[friend_id]['initiated'] += 1

    return params

#param: api object, params dictionary
#returns: updated params dictionary
#traverses all available mentions of the user, retrieving information on @reply mentions and updating params
def process_mentions(api, params):

    mentions = api.mentions(count=1000, include_entities = True)
    i=0

    for mention in mentions:

        (tweet_length, intimacy_count, links) = process_tweet(mention)
        friend_id = mention.user.id

        params[friend_id]['reply_words'] += tweet_length
        params[friend_id]['reply_intimacy_words'] += intimacy_count
        params[friend_id]['link_sharing'] += links
    
    return params

#param: api object, params dictionary
#returns: updated params dictionary
#goes through all direct messages sent by and receieved by the user 
def process_direct_msgs(api, params):

    for message in api.direct_messages(count=10000):
        print dir(message)
        break

    return params


def get_params(twitter_id):

    auth = tweepy.OAuthHandler("DYe0C4rw7VlDyRanFRrj3g", "9U74ene1QruXZIMbKAnSBbBRbfJ4YNkQCQvbrkGs")
    auth.set_access_token

    participant = Participant.objects.get(twitterid = twitter_id)

    auth.set_access_token(participant.oauth_token, participant.oauth_secret)
    api = tweepy.API(auth)

    params = {}

    for friend in api.friends_ids():

        params[friend] = { 'screen_name': api.get_user(friend).screen_name,
                                'last_comm':None, 
                                'first_comm':None, 
                                'reply_words':0, 
                                'reply_intimacy_words':0,
                                'initiated':0,
                                'link_sharing':0,
                                 'follower_count':0,
                                 'direct_messages':0}

        params[friend]['follower_count'] = api.get_user(friend).followers_count

    #iterating over statuses

    params = process_statuses(api, params)

    #iterating over mentions

    params = process_mentions(api, params)

    #iterating over rcvd/sent direct messages

    #params = process_direct_msgs(api,params)

    return params



   

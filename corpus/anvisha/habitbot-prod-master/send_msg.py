from django.core.management import setup_environ
from habitbot import settings
import tweepy

from bot.models import Message

setup_environ(settings)

def message_sender():
    # this uses the consumer key & secret for habitbot
    auth = tweepy.OAuthHandler("DYe0C4rw7VlDyRanFRrj3g", "9U74ene1QruXZIMbKAnSBbBRbfJ4YNkQCQvbrkGs")
    auth.set_access_token

    # iterate through all the pending stuff
    pending = Message.objects.filter(message_state__exact='PENDING')

    for msg in pending:
        auth.set_access_token(msg.message_sender.oauth_token, msg.message_sender.oauth_secret)
        api = tweepy.API(auth)
        try:
           api.update_status(status=msg.message_text, in_reply_to_status=msg.reply_to_id)
           msg.message_state='SENT'
           msg.save()
        except:
           msg.message_state='PENDING'
           msg.num_tries=msg.num_tries+1
# only try three times
           if msg.num_tries>2:
               msg.message_state='FAILED'
            msg.save()

from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from bot.models import *
import tweepy
import random


class Command(NoArgsCommand):
    help = 'Get all of the recent at-replies to habitbot from all of the users in the system'

    def handle_noargs(self, **options):
	print "hello i am broken"
   	
habitbot-prod
=============

##Habitbot is a twitter bot that helps you form and maintain habits.

To run the dev server on habitbot.csail.mit.edu: python manage.py runserver 128.30.44.249:8000
(I have a bash alias set up to run the dev server with just 'rundev')

Running locally will give you an error when you login, since we have to hardcode the url into twitter. Just change the habitbot part into localhost and you should be set.

To run this locally, you need to install some things:
-----------------------------------------------------
- (Make sure you have pip installed.)
- sudo pip install oauth2  # for authenticating users
- sudo pip install tweepy  # for interfacing with twitter easily, pingfriends does not work with the current version of tweepy
- sudo pip install django-chronograph # for cron management
- sudo pip install south   # for database migrations

###How to change the database:
python manage.py schemamigration bot --auto

###How to run tests:
- Tests should live in authentication/tests.py or bot/tests.py. Bot/tests.py has an example of what a test looks like.
- Run tests with python manage.py test; the command line arguments include:
- -- verbose=2 for quite verbose (verbose=3 is *very* verbose)
- *name of app, like bot* for testing only one test suite.
- Chronograph is, as of right now, throwing errors in its tests.

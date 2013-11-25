from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from authentication.views import twitter_login, twitter_logout, twitter_authenticated

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'habitbot.views.home', name='home'),
    # url(r'^habitbot/', include('habitbot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Copied from previous habitbot
    url(r'^login/?$', 'authentication.views.twitter_login', name='login'),
    url(r'^logout/?$', 'authentication.views.twitter_logout', name='logout'),
    url(r'^login/authenticated/?$', 'authentication.views.twitter_authenticated', name='authenticated'),
    url(r'^$', 'bot.views.home', name='home'), 
    url(r'^about/$', 'bot.views.about', name='about'), 
    url(r'^thanks/$', 'bot.views.thanks', name='thanks'), 
    url(r'^goals/$', 'bot.views.goal', name='new_goal'),
    url(r'^goals/(\d+)$', 'bot.views.goal', name='goal'),
    url(r'^contact/$', 'bot.views.contact', name='contact'),
    url(r'^entercode/$', 'bot.views.entercode', name='entercode'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^pingfriends/', 'bot.views.pingfriends', name='pingfriends'),

    #(r'^invites/', include('privatebeta.urls')),

)

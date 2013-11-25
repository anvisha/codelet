from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from retrieve_friends import get_friends

#from bot.models import Participant, Goal, Pageview, Update
from bot.models import *

from firsttweetpost import postfirsttweet

#base_template in case everything else fails. probably not a graceful choice.
base_template = "base.html"

def home(request, template_name="home.html"):
    if request.user.is_authenticated() and request.user.participant.invited:
        base_template = "if_in.html"
        print "home if in"
    elif request.user.is_authenticated() and not request.user.participant.invited:
        base_template = "auth_only.html"
        print "home auth only"
    else:
        base_template = "if_out.html"
        print "home if out"
    if request.user.is_authenticated() and request.user.participant.invited:
        participant = request.user.participant
        goals = participant.goals.all()
        #pageview = Pageview.objects.create(participant=participant,
        #   page_name="home.html",
        #   goal=None)
    else :
        participant = None
        goals = None
    return render_to_response(template_name, {
            'base_template': base_template,
            'participant' : participant,
            'goals' : goals,
        }, context_instance=RequestContext(request))

def about(request, template_name="about.html"):
    if request.user.is_authenticated() and request.user.participant.invited:
        base_template = "if_in.html"
        print "home if in"
    elif request.user.is_authenticated() and not request.user.participant.invited:
        base_template = "auth_only.html"
        print "home auth only"
    else:
        base_template = "if_out.html"
        print "home if out"
    if request.user.is_authenticated() and request.user.participant.invited:
        participant = request.user.participant
        goals = participant.goals.all()
    else :
        participant = None
        goals = None
    return render_to_response(template_name, {
            'base_template': base_template,
            'participant' : participant,
            'goals' : goals,
        }, context_instance=RequestContext(request))

def goal(request, goal_id=None, template_name="goal.html"):
    if request.user.is_authenticated() and request.user.participant.invited:
        base_template = "if_in.html"
    elif request.user.is_authenticated() and not request.user.participant.invited:
        base_template = "auth_only.html"
    else:
        base_template = "if_out.html"
    if request.user.is_authenticated() and request.user.participant.invited:
        participant = request.user.participant
        if goal_id:
            # changing an existing goal
            # new pageview
            goal = Goal.objects.get(id=goal_id)
            #pageview = Pageview.objects.create(participant=participant,
            #    page_name="goal.html",
            #    goal=goal)
            changed = False
            if request.method == "POST":
                update = Update(participant=participant, goal=goal)
                if goal.goalname != request.POST.get("goalname", goal.goalname):
                    goal.goalname = request.POST.get("goalname", goal.goalname)
                    update.goalname = goal.goalname
                    changed = True
                if goal.hashtag != request.POST.get("hashtag", goal.hashtag):
                    goal.hashtag = request.POST.get("hashtag", goal.hashtag)
                    update.hashtag = goal.hashtag
                    changed = True
                if goal.punishmsg != request.POST.get("punishmsg", goal.punishmsg):
                    goal.punishmsg = request.POST.get("punishmsg", goal.punishmsg)
                    update.punishmsg = goal.punishmsg
                    changed = True
                if goal.rewardmsg != request.POST.get("rewardmsg", goal.rewardmsg):
                    goal.rewardmsg = request.POST.get("rewardmsg", goal.rewardmsg)
                    update.rewardmsg = goal.rewardmsg
                    changed = True
                if goal.remindmsg != request.POST.get("remindmsg", goal.remindmsg):
                    goal.remindmsg = request.POST.get("remindmsg", goal.remindmsg)
                    update.remindmsg = goal.remindmsg
                    changed = True
                if goal.remind_tod != request.POST.get("remind_tod", goal.remind_tod):
                    goal.remind_tod = request.POST.get("remind_tod", goal.remind_tod)
                    update.remind_tod = goal.remind_tod
                    changed = True
                if goal.remind_dow != request.POST.get("remind_dow", goal.remind_dow):
                    goal.remind_dow = request.POST.get("remind_dow", goal.remind_dow)
                    update.remind_dow = goal.remind_dow
                    changed = True
                if goal.donttweet != request.POST.get("donttweet", goal.donttweet):
                    goal.donttweet = request.POST.get("donttweet", goal.donttweet)
                    update.donttweet = goal.donttweet
                    changed = True
                is_done_today = request.POST.get("is_done_today",False) == 'on'
                if goal.is_done_today != is_done_today:
                    goal.is_done_today = is_done_today
                    update.is_done_today = goal.is_done_today
                    changed = True
                is_paused = request.POST.get("is_paused",False) == "on"
                if goal.is_paused != is_paused:
                    goal.is_paused = is_paused
                    update.is_paused = goal.is_paused
                    changed = True
                goal.save()
                update.save() 
            return render_to_response(template_name, {
                    'base_template': base_template,
                    'participant' : participant,
                    'goal' : goal,
                    'changed' : changed,
                    }, context_instance=RequestContext(request))
        else:
            # makin' a new goal
            if request.method == "POST":
                print request.POST.get("firsttweet")
                goal = Goal.objects.create(participant=participant, 
                    goalname=request.POST.get("goalname", "No goal set"),
                    hashtag=request.POST.get("hashtag", "No hashtag set"),
                    punishmsg=request.POST.get("punishmsg", "No punishment set"),
                    rewardmsg=request.POST.get("rewardmsg", "No reward set"),
                    remindmsg=request.POST.get("remindmsg", "No reminder message set"),
                    remind_tod=request.POST.get("remind_tod", "No reminder time set"),
                    remind_dow=request.POST.get("remind_dow", "No reminder day set"),
                    donttweet=request.POST.get("donttweet", False),
                    firsttweet=request.POST.get("firsttweet", "This is a default tweet from @habitbot."),
                    )
                update = Update.objects.create(participant=participant, 
                    goal=goal,
                    goalname=goal.goalname,
                    hashtag=goal.hashtag,
                    punishmsg=goal.punishmsg,
                    rewardmsg=goal.rewardmsg,
                    donttweet=goal.donttweet,
                    firsttweet=goal.firsttweet,
                    )
                # post first tweet
                postfirsttweet(participant,goal)
                return HttpResponseRedirect('/goals/'+str(goal.id))
            else:
                """ Some sort of error, but it shouldn't really happen..."""
    else:
        return HttpResponseRedirect('/')

def entercode(request, template_name="entercode.html"):
    if request.user.is_authenticated() and request.user.participant.invited:
        base_template = "if_in.html"
    elif request.user.is_authenticated() and not request.user.participant.invited:
        base_template = "auth_only.html"
    else:
        base_template = "if_out.html"
    if request.method == 'POST':
        form = InviteForm(request.POST)
        warning = ""
        if form.is_valid():
            # this should definitely strip any whitespace
            # and strip the @ from the beginning of the twitterid if they put one there
            twitterid=request.POST.get("twitterid", "")
            enteredcode=request.POST.get("invitecode", "")
            twids=Invite.objects.filter(twitterid=twitterid)
            for twid in twids:
                correctcode=twid.invitecode
                inviteused=twid.inviteused
                p_objs = Participant.objects.filter(twitterid=twitterid)
                for p_obj in p_objs:
                    print "we found a participant:"
                    print p_obj.twitterid
                    p_obj.invited = True
                    p_obj.save()
                # now check to make sure they have the right invite code/email pair
                if not inviteused and enteredcode==correctcode :
                    twid.inviteused=True
                    twid.save()
                    return HttpResponseRedirect('/login/')
            # if they don't pass, reload the form with a warning.
            # this might be able to be handled with is_valid()
            form = InviteForm(initial={'twitterid':'@'})
            warning = "We don't have that email/invite pair on record."
    else: 
        form = InviteForm(initial={'twitterid':'@'})
        warning=""
    return render(request, 'entercode.html', {
            'base_template': base_template,
            'form': form,
            'warning': warning,
            })

def contact(request, template_name="contact.html"):
    if request.user.is_authenticated() and request.user.participant.invited:
        base_template = "if_in.html"
    elif request.user.is_authenticated() and not request.user.participant.invited:
        base_template = "auth_only.html"
    else:
        base_template = "if_out.html"
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            invite = Invite.objects.create(partname=request.POST.get("partname", "No name given"), 
                                           twitterid=request.POST.get("twitterid", "No twitterid given"),
                                           email=request.POST.get("email", "No email given"),
                                           habit=request.POST.get("habit", "No habit given")
                                           )
            return HttpResponseRedirect('/thanks/')
    else:
            form = ContactForm(initial={'twitterid':'@'})
    return render(request, 'contact.html', {
            'base_template': base_template,
            'form': form,
        })

def thanks(request, template_name="thanks.html"):
    return render(request, 'thanks.html')

def pingfriends(request, template_name="pingfriends.html"):
    if request.user.is_authenticated() and request.user.participant.invited:
        base_template = "if_in.html"
    elif request.user.is_authenticated() and not request.user.participant.invited:
        base_template = "auth_only.html"
    else:
        base_template = "if_out.html"
    friends_list = get_friends(request.user.participant.twitterid)
    #might not need this
    #template = loader.get_template('/templates/pingfriends.html')
    context = {'friends_list': friends_list,
               'base_template': base_template,}

    return render(request, 
                  template_name,
                  context,
                  )

    #return render_to_response(template_name, context, context_instance=RequestContext(request))

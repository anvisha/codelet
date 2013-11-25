# 6.00 Problem Set 5
#Name: Danielle Chow
#Collaborators(Discussion):Sammy Khalifa, Maddy Wharton, Tiffany Hood
#Collaborators (Identical Solution):
#Time:7.5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from Tkinter import *


#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory: #making new new instances
    def __init__(self, guid, title, subject, summary, link):
        self.guid=guid
        self.title=title
        self.subject=subject
        self.link=link
        self.summary=summary

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_link(self):
        return self.link

    def get_summary(self):
        return self.summary

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# WordTrigger
class WordTrigger(Trigger):
    def __init__(self,word):
        self.word=word.lower() #No longer case sensitive
    def is_word_in(self,text):
        text=text.lower() #Has to all be lowercase so the step above makes sense

        for symbol in string.punctuation:
            text=text.replace(symbol, ' ') #makes punctuation function as the end of a word

        wordlist=text.split() #makes a list of all "words"

        return self.word in wordlist #gives the true/false for if the word is in the text or not

#The below functions are possible, because they are passed back to WordTrigger

# TitleTrigger
class TitleTrigger(WordTrigger):
##    def __init__(self,word):
##        self.word=word.lower()
        
    def evaluate(self,story):
        return self.is_word_in(story.get_title())
        
# SubjectTrigger
class SubjectTrigger(WordTrigger):
    def evaluate(self,story):
        return self.is_word_in(story.get_subject())
    
# SummaryTrigger
class SummaryTrigger(WordTrigger):
    def evaluate(self,story):
        return self.is_word_in(story.get_summary())


# Composite Triggers
# Problems 6-8

# NotTrigger
class NotTrigger(Trigger):
    def __init__(self,trigger):
        self.trigger=trigger
        
    def evaluate(self,story): #making the search exclude certain characteristics to trigger
        return not self.trigger.evaluate(story)
    
# AndTrigger
class AndTrigger(Trigger):  #must have both characteristics to trigger
    def __init__(self, trigger1, trigger2):
        self.trigger1=trigger1
        self.trigger2=trigger2

    def evaluate(self,story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
    
# OrTrigger
class OrTrigger(Trigger): #must have one OR another characteristic to trigger
    def __init__(self, trigger1, trigger2):
        self.trigger1=trigger1
        self.trigger2=trigger2

    def evaluate(self,story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

# Phrase Trigger
# Question 9

# PhraseTrigger
class PhraseTrigger(Trigger):   #looks for an entire phrase by adding phrase to self
    def __init__(self,phrase):
        self.phrase=phrase

    def phrase_in_text(self,text):
        return self.phrase in text

    def evaluate(self,story):
        return self.phrase_in_text(story.get_subject()) or self.phrase_in_text(story.get_title()) or self.phrase_in_text(story.get_summary())
    #subject, title, summary 

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # Problem 10    #makes a list of stories that trigger by appending an initially empty list
    interesting_stories=[]
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                interesting_stories.append(story)
    return interesting_stories

#======================
# Part 4
# User-Specified Triggers
#======================

def makeTrigger(trigger_map, trigger_type, params, name):
    """
    Takes in a map of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and adds a new trigger
    to the trigger map dictionary.

    trigger_map: dictionary with names as keys (strings) and triggers as values
    trigger_type: string indicating the type of trigger to make (ex: "TITLE")
    params: list of strings with the inputs to the trigger constructor (ex: ["world"])
    name: a string representing the name of the new trigger (ex: "t1")

    Modifies trigger_map, adding a new key-value pair for this trigger.

    Returns: None
    """
    if trigger_type == "TITLE":
        trigger = TitleTrigger(params[0])

    elif trigger_type == "SUBJECT":
        trigger = SubjectTrigger(params[0])

    elif trigger_type == "SUMMARY":
        trigger = SummaryTrigger(params[0])

    elif trigger_type == "NOT":
        trigger = NotTrigger(trigger_map[params[0]])

    elif trigger_type == "AND":
        trigger = AndTrigger(trigger_map[params[0]], trigger_map[params[1]])

    elif trigger_type == "OR":
        trigger = OrTrigger(trigger_map[params[0]], trigger_map[params[1]])

    elif trigger_type == "PHRASE":
        trigger = PhraseTrigger(" ".join(params))

    else:
        return None

    trigger_map[name] = trigger
def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """

    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    triggers = []
    trigger_map = {}
    for line in lines:

        linesplit = line.split(" ")

        # Making a new trigger
        if linesplit[0] != "ADD":
            trigger = makeTrigger(trigger_map, linesplit[1],
                                  linesplit[2:], linesplit[0])

        # Add the triggers to the list
        else:
            for name in linesplit[1:]:
                triggers.append(trigger_map[name])

    return triggers
    
import thread

SLEEPTIME = 60 #seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    try:
        t1 = TitleTrigger("Syria")
        t2 = SubjectTrigger("Iran")
        t3 = PhraseTrigger("Wall Street")
        t4 = OrTrigger(t2, t3)
        triggerlist = [t1, t4]
        
        # Problem 11
        # After updating triggers.txt, uncomment the line below
        triggerlist = readTriggerConfig("triggers.txt")

        # from here is about drawing
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=frame.quit)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_summary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print "Polling . . .",
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            map(get_cont, stories)
            scrollbar.config(command=cont.yview)


            print "Sleeping..."
        time.sleep(SLEEPTIME)

    except Exception as e:
        print e


if __name__ == '__main__':

    root = Tk()
    root.title("Some RSS parser")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()


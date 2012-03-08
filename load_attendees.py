#!/usr/bin/env python

import sys, os
import re
import json

from django_bootstrap import bootstrap
bootstrap(__file__)

from attendees.models import Attendee, Event

def eb_questions(attendee):
    a = {}
    answers = attendee['answers']
    for answer in answers:
        a["%s" % answer['answer']['question_id']] = answer['answer']['answer_text'].strip()
    return a

tw_url = re.compile(r'^(?:(?:https?://){0,3}(?:www\.)?twitter\.com/(?:\#\!/)?@?|@?)([^/:\#\!]+)/?#?$', re.I)
def filter_twitter(twitter):
    twitter_id = None
    twitter.strip()
    m = tw_url.match(twitter)
    if m:
        twitter_id = m.group(1)
    else:
        #sys.stderr.write("could not extract twitter ID from '%s'" % twitter)
        pass
    return twitter_id

site_url = re.compile(r'^(?:(?:http://)?(https?://))?([^\s]+)',re.I)
def filter_site(site):
    m = site_url.match(site)
    if m:
        proto = m.group(1)
        if not proto:
            proto = "http://"
        return proto + m.group(2)
    else:
        pass
        #sys.stderr.write("could not extract website from '%s'" % site)
    return None

def filter_tags(tags):
    return map(lambda t: t.strip(), tags.split(','))

def load_attendees(event, doc):

    attendees = doc['attendees']
    for attendeeObj in attendees:
        attendee = attendeeObj['attendee']
        eb_id = attendee['id']
        try:
            a = Attendee.objects.get(eb_id=eb_id)
        except Attendee.DoesNotExist:
            a = Attendee()
            a.eb_id = eb_id
        a.first_name = attendee['first_name'].strip()
        a.last_name = attendee['last_name'].strip()
        #print "%s %s" % (a.first_name, a.last_name)
        answers = eb_questions(attendee)
        if '957323' in answers:
            twitter = filter_twitter(answers['957323'].split(',')[0])
            if twitter:
                a.twitter = twitter
        if '957329' in answers:
            site = filter_site(answers['957329'].split(',')[0])
            if site:
                a.website = site
        if '957327' in answers:
            a.affiliation = answers['957327']
            
        a.save()
        # now add the relations
        if '957331' in answers:
            tags = filter_tags(answers['957331'].lower())
            a.tags.set(*tags)
        a.events.add(event)

if __name__ == "__main__":
    load_attendees(json.load(open(sys.argv[1])))

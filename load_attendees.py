#!/usr/bin/env python

import sys
import re
import json

from django_bootstrap import bootstrap
bootstrap(__file__)

from attendees.models import Attendee

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
        # bcb6 if '957323' in answers:
        if '1965641' in answers:
            twitter = filter_twitter(answers['1965641'].split(',')[0])
            if twitter:
                a.twitter = twitter
        # bcb6 if '957329' in answers:
        if '1965653' in answers:
            site = filter_site(answers['1965653'].split(',')[0])
            if site:
                a.website = site
        # bcb6 if '957327' in answers:
        if '1965645' in answers:
            a.affiliation = answers['1965645']
            
        a.save()
        # now add the relations
        # bcb6 if '957331' in answers:
        if '1965659' in answers:
            tags = filter_tags(answers['1965659'].lower())
            a.tags.set(*tags)
        a.events.add(event)

if __name__ == "__main__":
    load_attendees(json.load(open(sys.argv[1])))

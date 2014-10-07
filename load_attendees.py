#!/usr/bin/env python

import sys
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

def load_attendees(event, doc, config):
    attendees = doc['attendees']
    ebq = config['eventbrite']['questions']
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
        a.email = attendee['email'].strip()
        if 'website' in attendee:
            site = filter_site(attendee['website'].split(',')[0])
            if site:
                a.website = site
        #print "%s %s" % (a.first_name, a.last_name)
        answers = eb_questions(attendee)
        if ebq['twitter'] in answers:
            twitter = filter_twitter(answers[ebq['twitter']].split(',')[0])
            if twitter:
                a.twitter = twitter
        if 'site' in ebq and ebq['site'] in answers:
            site = filter_site(answers[ebq['site']].split(',')[0])
            if site:
                a.website = site
        if ebq['affiliation'] in answers:
            a.affiliation = answers[ebq['affiliation']]
        a.save()
        # now add the relations
        if ebq['tags'] in answers:
            tags = filter_tags(answers[ebq['tags']].lower())
            a.tags.set(*tags)
        a.events.add(event)

if __name__ == "__main__":
    with open(sys.argv[1]) as attendee_doc_file:
        with open(sys.argv[2]) as config_file:
            attendee_doc = json.load(attendee_doc_file)
            config = json.load(config_file)
            load_attendees(Event.objects.get(slug=sys.argv[3]), attendee_doc, config)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django_bootstrap import bootstrap

# put the path of the faces website here
bootstrap("../../barcampboston/")

from attendees.models import Event

from make_pdf import MakePdf
import urllib
import os
import sys
import unicodedata

#####################################################################
#
# This takes all the attendees who are in the Django database and 
# makes PDF namebadges for them. 
# 
# This also generates blank badges with individual QR code numbers
# on them.
#
#####################################################################
#
# requires Inkscape
#
# makes network calls to generate the QR code using Google's chart API
#
#####################################################################
#
# configuration
#################

# select which template you'd like to use.
#svg_file = "templates/badge_3x4.svg"
svg_file = "badge_8x13_cropmark.svg"

# output directory where generated PDFs will be stored.
outdir = "badges"

# the slug name of the event
event = "barcampboston7"

#####################################################################

def strip_accents(s):
    return u''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def get_filename(params):
    return "%s/%s_%s_%s.pdf" % (outdir, params['last_name'], params['first_name'], params['eb_id'])

def make_mecard(attendee):
    #name = strip_accents("%s %s" % (attendee.first_name, attendee.last_name))
    name = u"%s %s" % (attendee.first_name, attendee.last_name)
    print "Generating card for %s..." % name
    mecard = u"MECARD:N:%s;" % name
    if attendee.affiliation:
        mecard += u"ORG:%s;" % attendee.affiliation
    if attendee.website and attendee.twitter:
        mecard += u"URL:%s;NOTE:http://twitter.com/%s;" % (attendee.website, attendee.twitter)
    elif attendee.twitter:
        mecard += u"URL:http://twitter.com/%s;" % attendee.twitter
    elif attendee.website:
        mecard += u"URL:%s;" % attendee.website
    mecard += u"EBID:%s;" % attendee.eb_id
    mecard += u";"
#    mecard = strip_accents(mecard)
    mecard = mecard.encode('utf-8')
    print mecard
    qrcode_url = u'http://chart.apis.google.com/chart?%s' % urllib.urlencode({"cht": u"qr", "chs": u"350x350", u"chl": mecard})
    return qrcode_url

if __name__ == '__main__':
    mkpdf = MakePdf('badge', svg_file)
    if len(sys.argv) > 1:
        p = sys.argv[1]
        from django.db.models import Q
        query = Q(first_name__icontains=p) | Q(last_name__icontains=p)
        attendees = Event.objects.get(slug=event).attendee_set.filter(query)
        make_blanks = False
    else:
        attendees = Event.objects.get(slug=event).attendee_set.all()
        make_blanks = True
    for attendee in attendees:
        qrcode_url = make_mecard(attendee)
        qrcode_file = "qrcode.png"
        tags = attendee.tags.all()
        params = {
            "first_name": attendee.first_name, 
            "last_name": attendee.last_name,
            'eb_id': attendee.eb_id,
            'affiliation': attendee.affiliation or u"",
            'twitter': attendee.twitter or u"",
            'website': attendee.website or u"",
            'qrcode':qrcode_file,
            'patron': attendee.patron,
            'sponsor': attendee.sponsor,
            'tags': tags
            }

        if os.path.isfile("./"+get_filename(params)):
            print "skipping"
            continue
        urllib.urlretrieve(qrcode_url, qrcode_file)
        mkpdf.make_pdf(params, get_filename(params))

    if make_blanks:
        print "Generating serialized blanks..."
        for i in range(0,200):
            mecard = "BCB7:%d" % i
            qrcode_url = u'http://chart.apis.google.com/chart?%s' % urllib.urlencode({"cht": u"qr", "chs": u"350x350", u"chl": mecard})
            qrcode_file = "qrcode.png"
            urllib.urlretrieve(qrcode_url, qrcode_file)
            params = {
                'last_name': "______________",
                'first_name': '______________',
                'eb_id': "extra_%d" % i,
                'tags': ['__________', '__________', '__________'],
                'qrcode': qrcode_file,
            }
            mkpdf.make_pdf(params, get_filename(params))

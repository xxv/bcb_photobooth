#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django_bootstrap import bootstrap

# put the path of the faces website here
bootstrap("../../barcampboston/")

from attendees.models import Event

from make_pdf import MakePdf
import urllib
import os
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
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def get_filename(params):
    return "%s/%s_%s_%s.pdf" % (outdir, params['last_name'], params['first_name'], params['eb_id'])

if __name__ == '__main__':
    mkpdf = MakePdf('badge', svg_file)
    for attendee in Event.objects.get(slug=event).attendee_set.all():
        name = strip_accents("%s %s" % (attendee.first_name, attendee.last_name))
        print "Generating card for %s..." % name
        mecard = "MECARD:N:%s;" % name
        if attendee.affiliation:
            mecard += "ORG:%s;" % attendee.affiliation
        if attendee.website and attendee.twitter:
            mecard += "URL:%s;NOTE:http://twitter.com/%s;" % (attendee.website, attendee.twitter)
        elif attendee.twitter:
            mecard += "URL:http://twitter.com/%s;" % attendee.twitter
        elif attendee.website:
            mecard += "URL:%s;" % attendee.website
        mecard += "EBID:%s;" % attendee.eb_id
        mecard += ";"
        tags = attendee.tags.all()
        mecard = strip_accents(mecard)
        print mecard
        qrcode_url = 'http://chart.apis.google.com/chart?cht=qr&chs=350x350&chl=%s' % urllib.quote(mecard)
        qrcode_file = "qrcode.png"
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

    print "Generating serialized blanks..."
    for i in range(0,100):
        mecard = "BCB6:%d" % i
        qrcode_url = 'http://chart.apis.google.com/chart?cht=qr&chs=350x350&chl=%s' % urllib.quote(mecard)
        qrcode_file = "qrcode.png"
        urllib.urlretrieve(qrcode_url, qrcode_file)
        params = {
            'lastname': "",
            'firstname': '',
            'eb_id': "extra_%d" % i
        }
        mkpdf.make_pdf(params, get_filename(params))

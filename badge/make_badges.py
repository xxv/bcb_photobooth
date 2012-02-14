#!/usr/bin/python
# -*- coding: utf-8 -*-
from django_bootstrap import bootstrap

# put the path of the faces website here
bootstrap("../photo_booth/site/barcampboston/")

from attendees.models import Attendee

from make_pdf import make_pdf
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

xslt_file = "edit_badge.xsl"

# select which template you'd like to use.
#svg_file = "templates/badge_3x4.svg"
svg_file = "templates/badge_3x4_cropmark.svg"

# output directory where generated PDFs will be stored.
outdir = "badges_cropmark"

#####################################################################

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def get_filename(params):
    return "%s/%s_%s_%s.pdf" % (outdir, params['lastname'], params['firstname'], params['eb_id'])

if __name__ == '__main__':
    mkpdf = MakePdf(xslt_file, svg_file)
    for attendee in Attendee.objects.all():
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
            "firstname": attendee.first_name, 
            "lastname": attendee.last_name,
            'eb_id': attendee.eb_id,
            'org': attendee.affiliation or "",
            'twitter': attendee.twitter or "",
            'website': attendee.website or "",
            'qrcode':qrcode_file
            }
        i = 1
        for tag in tags[:3]:
            params['tag%d' % i] = tag
            i+=1

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

#!/usr/bin/env python

import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, json, sys, os
import datetime

from django_bootstrap import bootstrap
bootstrap(__file__)

from django.core.exceptions import ObjectDoesNotExist

from barcampboston.attendees.models import Room, TimeSlot, Talk

try:
    from local_gdoc_settings import *
except:
    pass

def add_rooms(row):
    for room_name, capacity in row.items():
        if room_name != 'time':
            try:
                room = Room.objects.get(name=room_name)
            except ObjectDoesNotExist:
                print "no room, adding one"
                print room_name
                print capacity
                if capacity != None and room_name != None:
                    room = Room(name=room_name, capacity=capacity)
                    room.save()

def add_timeslots_and_talks(row):
    print row
    ts_name = row['time']
    try:
        timeslot = TimeSlot.objects.get(name=ts_name)
    except ObjectDoesNotExist:
        print "no timeslot, adding one"
        if talk_name != None and room_name != None:
            timeslot = TimeSlot(name=ts_name)
            timeslot.save()
    for room_name, talk_name in row.items():
        print "room" 
        print room_name
        print ts_name
        if room_name != 'time':
            try:
                talk = Talk.objects.get(name=talk_name)
            except ObjectDoesNotExist:
                room = Room.objects.get(name=room_name)
                time = TimeSlot.objects.get(name=ts_name)
                talk = Talk(name=talk_name, room=room, time=time)
                talk.save()

# Connect to Google
gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = username
gd_client.password = password
gd_client.source = source
gd_client.ProgrammaticLogin()

q = gdata.spreadsheet.service.DocumentQuery()
q['title'] = doc_name
q['title-exact'] = 'true'
feed = gd_client.GetSpreadsheetsFeed(query=q)
spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]

rows = gd_client.GetListFeed( spreadsheet_id, worksheet_id ).entry

for entry in rows:
    entrydict = dict(zip(
        entry.custom.keys(), 
        [ value.text for value in entry.custom.values() ] 
    ))
    print entrydict['time']
    if entrydict['time'] == None:
        print 'adding rooms'
        add_rooms(entrydict)
    else:
        print 'adding timeslot and talks'
        add_timeslots_and_talks(entrydict)


    print entrydict    


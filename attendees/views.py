import json
import sys

import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.generic import list_detail
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt 

from taggit.models import Tag
from djutils.decorators import async
from sorl import thumbnail

from attendees.forms import AttendeeForm
from attendees.models import Attendee, Event

# Get an instance of a logger
logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def show_event_attendee_by_letter(request, event_slug, letter=None):
    event = get_object_or_404(Event.objects, slug=event_slug)
    queryset = event.attendee_set.all().extra(select={'lower_name': 'lower(last_name)'}).order_by('lower_name')
    if letter:
        queryset = queryset.filter(last_name__istartswith=letter)

    return list_detail.object_list(
            request,
            queryset = queryset,
            template_name = "attendees/attendee_list_by_letter.html",
            template_object_name = "attendee",
            extra_context = {
                "event": event,
                "current_letter": letter,
                 "letters": [chr(n) for n in range(ord('a'), ord('z')+1)]}
            )

@require_http_methods(["GET"])
def show_tag(request, tagslug):
    tag = get_object_or_404(Attendee.tags, slug=tagslug)

    return list_detail.object_list(
            request,
            queryset = Attendee.objects.filter(tags__in=[tag]),
            template_name = "attendees/attendee_list_by_tag.html",
            template_object_name = "attendee",
            extra_context = {
                "tag": tag,
                }
            )

@require_http_methods(["POST"])
@csrf_exempt
def upload_photo(request, eb_id=None, id=None):
    if id:
        attendee = get_object_or_404(Attendee, id=id)
    elif eb_id:
        attendee = get_object_or_404(Attendee, eb_id=eb_id)
    else:
        raise Exception("missing parameter")
    photo = request.FILES['photo']
    if not photo:
        return HttpResponseBadRequest("missing photo")
    if attendee.photo:
        thumbnail.delete(attendee.photo.name, delete_file=False)
    attendee.photo.save(photo.name, photo)
    photo_url = attendee.photo.url
    return HttpResponse(json.dumps({
        'eb_id': attendee.eb_id,
        'id': attendee.id,
        'first_name': attendee.first_name,
        'last_name': attendee.last_name,
        'photo': photo_url}), mimetype='application/json')


        
@require_http_methods(["GET"])
def get_attendee(request, eb_id=None, id=None):
    if id:
        attendee = get_object_or_404(Attendee, id=id)
    elif eb_id:
        attendee = get_object_or_404(Attendee, eb_id=eb_id)
    else:
        raise Exception("missing parameter")
    photo = None
    if attendee.photo:
        photo = attendee.photo.url
    return HttpResponse(json.dumps({
        'eb_id': attendee.eb_id,
        'id': attendee.id,
        'first_name': attendee.first_name,
        'last_name': attendee.last_name,
        'photo': photo}), mimetype='application/json')


@require_http_methods(["GET", "POST"])
@csrf_exempt
def attendee_view(request):
    if request.method == "GET":
        return get_attendees(request)
    elif request.method == "POST":
        return create_attendee(request)

def get_attendees(request):
    attendees = []
    for attendee in Attendee.objects.all():
        attendees.append({'first_name': attendee.first_name, 'last_name': attendee.last_name, 'org': attendee.affiliation or ""})
    return HttpResponse(json.dumps(attendees))

def create_attendee(request):
    form = AttendeeForm(request.POST)

    if form.is_valid():
        a = form.save()
        resp = HttpResponse("created", status=201)
        #resp['location'] = 
        return resp
    else:
        return HttpResponseBadRequest("form not valid")

@require_http_methods(["POST"])
@csrf_exempt
def sync(request):
    perform_sync()
    return HttpResponse("Starting sync...\n")

@async
def perform_sync():
    from eventbrite import EventbriteClient
    from load_attendees import load_attendees
    from attendees.models import EventbriteConfig

    eb = EventbriteConfig.objects.all()[0]

    ebc = EventbriteClient(eb.apikey, eb.userkey)
    loaded = []
    for event in eb.sync_events.all():
        try:
            attendees = ebc.list_event_attendees(event_id=int(event.eb_id))
            load_attendees(event, attendees)
            loaded.append(event.title)
        except RuntimeError as e:
            logger.error("error loading event %s: %s\n" % (event, e))
    logger.info("successfully loaded attendees for all events: %s." % (", ".join(loaded)))


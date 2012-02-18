from django.conf.urls.defaults import *
from django.views.generic import list_detail
from taggit.views import tagged_object_list
from attendees.views import show_tag, sync, get_attendee, upload_photo, attendee_view, show_event_attendee_by_letter

from barcampboston.attendees.models import Attendee, Event

event_info = {
    "queryset": Event.objects.all().order_by("-start_date"),
    "template_object_name": "event",
    }

urlpatterns = patterns('',
    # web
    url(r'^/?$', list_detail.object_list, event_info, name="latest_event"),
    url(r'^/?event/(?P<event_slug>[\w-]+)/?$', show_event_attendee_by_letter, name="event_detail"),
    url(r'^/?event/(?P<event_slug>[\w-]+)/(?P<letter>\w)/?$', show_event_attendee_by_letter, name="event_attendees_by_letter"),
    url(r'^/?topic/(?P<tagslug>[\w-]+)/?$', show_tag, name="tag"),
    # API
    url(r'^/?sync/?$', sync, name="sync"),
    url(r'^/?attendee/?$', attendee_view, name="create_attendee"),
    url(r'^/?attendee/ebid:(?P<eb_id>[\d]+)/?$', get_attendee, name="get_attendee"),
    url(r'^/?attendee/ebid:(?P<eb_id>[\d]+)/photo$', upload_photo, name="upload_photo"),
    url(r'^/?attendee/(?P<id>[\d]+)/?$', get_attendee, name="attendee_view"),
    url(r'^/?attendee/(?P<id>[\d]+)/photo$', upload_photo, name="upload_photo"),
)

from django.forms import ModelForm
from attendees.models import Attendee

class AttendeeForm(ModelForm):
    class Meta:
        model = Attendee

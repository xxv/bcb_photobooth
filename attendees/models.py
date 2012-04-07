from django.db import models

from taggit.managers import TaggableManager

class Attendee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    eb_id = models.IntegerField("EventBrite ID", blank=True, null=True)
    events = models.ManyToManyField('Event', blank=True, null=True)

    email = models.EmailField(max_length=255, blank=True, null=True)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField('Twitter ID', max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    sponsor = models.BooleanField(default=False)
    patron = models.BooleanField(default=False)

    tags = TaggableManager(blank=True)

    def name(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def event_names(self):
        return u", ".join([event.title for event in self.events.all()])

    class Meta:
        ordering = ["last_name"]

    def __unicode__(self):
        return self.name()

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    eb_id = models.IntegerField(blank=True, null=True)

    website = models.CharField(max_length=255, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

class EventbriteConfig(models.Model):
    apikey = models.CharField(max_length=16)
    userkey = models.CharField(max_length=20)
    sync_events = models.ManyToManyField('Event', blank=True, null=True, verbose_name="events to sync with Eventbrite")

class Room(models.Model):
    name = models.CharField(max_length=200)
    #slug = models.SlugField(blank=True, null=True) #TODO cazbot forgets how to auto-generate slug from name
    capacity = models.IntegerField()

    def __unicode__(self):
        return self.name

class TimeSlot(models.Model):
    name = models.CharField(max_length=100)
    #start_time = models.DateTimeField()
    #end_time = models.DateTimeField()

    def __unicode__(self):
        return self.name

    def isActive(self):
        #TODO return now() > start_time && < end_time ?
        return True

class Talk(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room)
    time = models.ForeignKey(TimeSlot)
    host = models.ManyToManyField(Attendee)

    def __unicode__(self):
        return self.name

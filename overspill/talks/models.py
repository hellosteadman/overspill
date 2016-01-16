from __future__ import absolute_import
from django.db import models
from django.contrib.auth.models import User
from . import EVENT_STATES, EVENT_STATE_CHOICES, helpers


class Event(models.Model):
    """
    An event, or a series of talks. Each event has a start and end date, for
    multiday events like DjangoCon.
    """

    creator = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30, unique=True)
    date_from = models.DateField()
    date_to = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('-date_from', 'name',)


class Talk(models.Model):
    """
    A talk that was meant to be given at an event, but for which there wasn't
    enough time.
    """

    event = models.ForeignKey(Event, related_name='talks')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=30)
    creator = models.ForeignKey(User)
    speaker_name = models.CharField(max_length=100, blank=True)
    slideshow = models.FileField(max_length=255,
                                 upload_to=helpers.set_talk_slideshow_url
                                 )

    uploaded = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=EVENT_STATE_CHOICES)

    def __unicode__(self):
        return self.title

    class Meta:
        unique_together = ('slug', 'event')
        ordering = ('-uploaded', 'slug')


class Slide(models.Model):
    """
    A single slide in a user's talk, as taken from the original slideshow file
    """

    talk = models.ForeignKey(Talk, related_name='slides')
    number = models.PositiveIntegerField()
    image = models.ImageField(max_length=255,
                              upload_to=helpers.set_slide_image_url
                              )

    notes = models.TextField(blank=True)
    audio = models.FileField(max_length=255, blank=True,
                             upload_to=helpers.set_slide_audio_url
                             )

    class Meta:
        unique_together = ('number', 'talk')
        ordering = ('number',)


class Link(models.Model):
    """
    A link to further, pertinent information for the talk
    """

    talk = models.ForeignKey(Talk, related_name='links')
    url = models.URLField(max_length=255)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ('order',)

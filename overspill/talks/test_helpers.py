from __future__ import absolute_import
from django.test import TestCase
from mock import Mock, patch
from time import mktime
from datetime import datetime
from django.contrib.auth.models import User
from .models import Event, Talk, Slide
from . import helpers

mock_time = Mock()
mock_time.return_value = mktime(datetime(2016, 1, 16, 0, 0, 0).timetuple())


class UniqueIDTest(TestCase):
    @patch('time.time', mock_time)
    def test_unique_id(self):
        """
        Test that unique_id() returns a value which is basically a hash of the
        current Unix timestamp, given in this case that it's midnight on the
        16th January 2016.
        """

        self.assertEqual(helpers.unique_id(), '339e1202740000')


class SetTalkSlideshowURLTest(TestCase):
    @patch('time.time', mock_time)
    def test_set_talk_slideshow_url(self):
        """
        Test that the slideshow filename helper function returns a filename
        derived from the talk ID, username, current timestamp and the uploaded
        slideshow file itself.
        """

        user = User.objects.create(username='foo')
        talk = Talk.objects.create(
            event=Event.objects.create(
                creator=user,
                name='DjangoCon EU 2016',
                slug='djangocon-eu-2016',
                date_from=datetime(2016, 3, 30).date(),
                date_to=datetime(2016, 4, 1).date()
            ),
            title='10 Things I Hate About PHP',
            slug='10-things',
            creator=user,
            slideshow='My Presentation.key'
        )

        self.assertEqual(
            helpers.set_talk_slideshow_url(talk,
                                           'My Presentation.key'
                                           ),
            'events/%d/talks/foo_339e1202740000.key' % talk.event.pk
        )


class SetSlideImageURLTest(TestCase):
    def test_set_slide_image_url(self):
        """
        Test that the slideshow filename helper function returns a filename
        derived from the talk ID, slide number and the attached slide image
        file itself.
        """

        user = User.objects.create(username='foo')
        slide = Slide.objects.create(
            talk=Talk.objects.create(
                event=Event.objects.create(
                    creator=user,
                    name='DjangoCon EU 2016',
                    slug='djangocon-eu-2016',
                    date_from=datetime(2016, 3, 30).date(),
                    date_to=datetime(2016, 4, 1).date()
                ),
                title='10 Things I Hate About PHP',
                slug='10-things',
                creator=user,
                slideshow='My Presentation.key'
            ),
            image='slide-1.png'
        )

        self.assertEqual(
            helpers.set_slide_image_url(slide, 'slide-1.png'),
            'events/%d/talks/slides/%d_1.png' % (
                slide.talk.event.pk, slide.talk.pk
            )
        )

    def test_set_slide_image_url_autoincrement(self):
        """
        Test that the slideshow filename helper function returns a filename
        derived from the talk ID, slide number and the attached slide image
        file itself, with an autoincrementing slide number.
        """

        user = User.objects.create(username='foo')
        talk = Talk.objects.create(
            event=Event.objects.create(
                creator=user,
                name='DjangoCon EU 2016',
                slug='djangocon-eu-2016',
                date_from=datetime(2016, 3, 30).date(),
                date_to=datetime(2016, 4, 1).date()
            ),
            title='10 Things I Hate About PHP',
            slug='10-things',
            creator=user,
            slideshow='My Presentation.key'
        )

        slide1 = Slide.objects.create(talk=talk, image='slide-1.png')
        slide2 = Slide.objects.create(talk=talk, image='slide-2.png')

        self.assertEqual(
            helpers.set_slide_image_url(slide1, 'slide-1.png'),
            'events/%d/talks/slides/%d_1.png' % (
                talk.event.pk, talk.pk
            )
        )

        self.assertEqual(
            helpers.set_slide_image_url(slide2, 'slide-2.png'),
            'events/%d/talks/slides/%d_2.png' % (
                talk.event.pk, talk.pk
            )
        )


class SetSlideAudioURLTest(TestCase):
    def test_set_slide_audio_url(self):
        """
        Test that the slideshow filename helper function returns a filename
        derived from the talk ID, slide number and the attached slide audio
        file itself.
        """

        user = User.objects.create(username='foo')
        slide = Slide.objects.create(
            talk=Talk.objects.create(
                event=Event.objects.create(
                    creator=user,
                    name='DjangoCon EU 2016',
                    slug='djangocon-eu-2016',
                    date_from=datetime(2016, 3, 30).date(),
                    date_to=datetime(2016, 4, 1).date()
                ),
                title='10 Things I Hate About PHP',
                slug='10-things',
                creator=user,
                slideshow='My Presentation.key'
            ),
            image='slide-1.mp3'
        )

        self.assertEqual(
            helpers.set_slide_audio_url(slide, 'slide-1.mp3'),
            'events/%d/talks/slides/%d_1.mp3' % (
                slide.talk.event.pk, slide.talk.pk
            )
        )

    def test_set_slide_audio_url_autoincrement(self):
        """
        Test that the slideshow filename helper function returns a filename
        derived from the talk ID, slide number and the attached slide audio
        file itself, with an autoincrementing slide number.
        """

        user = User.objects.create(username='foo')
        talk = Talk.objects.create(
            event=Event.objects.create(
                creator=user,
                name='DjangoCon EU 2016',
                slug='djangocon-eu-2016',
                date_from=datetime(2016, 3, 30).date(),
                date_to=datetime(2016, 4, 1).date()
            ),
            title='10 Things I Hate About PHP',
            slug='10-things',
            creator=user,
            slideshow='My Presentation.key'
        )

        slide1 = Slide.objects.create(talk=talk, image='slide-1.png')
        slide2 = Slide.objects.create(talk=talk, image='slide-2.png')

        self.assertEqual(
            helpers.set_slide_audio_url(slide1, 'slide-1.mp3'),
            'events/%d/talks/slides/%d_1.mp3' % (
                talk.event.pk, talk.pk
            )
        )

        self.assertEqual(
            helpers.set_slide_audio_url(slide2, 'slide-2.mp3'),
            'events/%d/talks/slides/%d_2.mp3' % (
                talk.event.pk, talk.pk
            )
        )

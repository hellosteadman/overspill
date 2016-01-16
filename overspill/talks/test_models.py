from __future__ import absolute_import
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from datetime import date
from .models import Event, Talk, Slide, Link


class EventTest(TestCase):
    """
    Tests for the `talks.Event` model.
    """

    def setUp(self):
        """
        Create a user that we can assign events to.
        """

        self.user, created = User.objects.get_or_create(username='foo')

    def create_event(self):
        """
        Utility function to create an event.
        """

        return Event.objects.create(
            creator=self.user,
            name='DjangoCon EU 2016',
            slug='djangocon-eu-2016',
            date_from=date(2016, 3, 30),
            date_to=date(2016, 4, 1)
        )

        return event

    def test_create(self):
        """
        Create an event, and test that the number of events in the database is
        1, and that the unicode function correclty returns the event name.
        """

        self.create_event()
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(unicode(Event.objects.get()), u'DjangoCon EU 2016')

    def test_unique_slug(self):
        """
        Create an event, and test that an integrity error is raised when trying
        to create an event with the same slug.
        """

        self.create_event()
        with self.assertRaises(IntegrityError):
            self.create_event()

    def test_update(self):
        """
        Update the created event, and make sure that the returned number of
        updated rows is 1.
        """

        event = self.create_event()
        update = Event.objects.filter(pk=event.pk).update(
            name='DjangoCon EU 2017',
            slug='djangocon-eu-2017',
            date_from=date(2017, 3, 30),
            date_to=date(2017, 4, 1)
        )

        self.assertEqual(update, 1)

    def test_delete(self):
        """
        Delete a newly-created event, and make sure the number of events in the
        database is 0.
        """

        event = self.create_event()
        Event.objects.get(pk=event.pk).delete()
        self.assertEqual(Event.objects.count(), 0)


class TalkTest(TestCase):
    """
    Tests for the `talks.Talk` model
    """

    def setUp(self):
        """
        Create an event that we can assign talks to.
        """

        user, created = User.objects.get_or_create(username='foo')
        self.event_one, created = Event.objects.get_or_create(
            creator=user,
            name='DjangoCon EU 2016',
            slug='djangocon-eu-2016',
            date_from=date(2016, 3, 30),
            date_to=date(2016, 4, 1)
        )

        self.event_two, created = Event.objects.get_or_create(
            creator=user,
            name='DjangoCon US 2016',
            slug='djangocon-us-2016',
            date_from=date(2016, 8, 1),
            date_to=date(2016, 8, 3)
        )

    def create_talk(self, event=None):
        """
        Utility function for creating talks.
        """

        return Talk.objects.create(
            event=event or self.event_one,
            title='10 Things I Hate About PHP',
            slug='10-things',
            creator=(event or self.event_one).creator,
            slideshow=SimpleUploadedFile('My Presentation.key',
                                         'binary data'
                                         )
        )

    def test_create(self):
        """
        Create a talk, and test that the number of talks in the database is 1,
        and that the unicode function correclty returns the talk name.
        """

        self.create_talk()
        self.assertEqual(Talk.objects.count(), 1)
        self.assertEqual(unicode(Talk.objects.get()),
                         u'10 Things I Hate About PHP'
                         )

    def test_unique_slug_per_event(self):
        """
        Create a talk for an event, and test that an integrity error is raised
        when trying to create a talk with the same slug, under the same event.
        """

        self.create_talk()
        with self.assertRaises(IntegrityError):
            self.create_talk()

    def test_unique_slug_event_combo(self):
        """
        Create a talk, and test that a second talk can be created with the same
        name as the first, as long as they're under different events.
        """

        self.create_talk()
        self.create_talk(self.event_two)

    def test_update(self):
        """
        Update the created talk, and make sure that the returned number of
        updated rows is 1.
        """

        talk = self.create_talk()
        update = Talk.objects.filter(pk=talk.pk).update(
            title='11 Things I Hate About PHP',
            slug='11-things',
        )

        self.assertEqual(update, 1)

    def test_delete(self):
        """
        Delete a newly-created talk, and make sure the number of talks in the
        database is 0.
        """

        talk = self.create_talk()
        Talk.objects.get(pk=talk.pk).delete()
        self.assertEqual(Talk.objects.count(), 0)


class SlideTest(TestCase):
    """
    Tests for the `talks.Slide` model
    """

    def setUp(self):
        """
        Create a talk that we can assign slides to.
        """

        user, created = User.objects.get_or_create(username='foo')
        self.talk_one, created = Talk.objects.get_or_create(
            event=Event.objects.create(
                creator=user,
                name='DjangoCon EU 2016',
                slug='djangocon-eu-2016',
                date_from=date(2016, 3, 30),
                date_to=date(2016, 4, 1)
            ),
            title='10 Things I Hate About PHP',
            slug='10-things',
            creator=user,
            slideshow=SimpleUploadedFile('My Presentation.key',
                                         'binary data'
                                         )
        )

        self.talk_two, created = Talk.objects.get_or_create(
            event=Event.objects.create(
                creator=user,
                name='DjangoCon US 2016',
                slug='djangocon-us-2016',
                date_from=date(2016, 8, 1),
                date_to=date(2016, 8, 3)
            ),
            title='10 Things I Hate About Java',
            slug='10-things',
            creator=user,
            slideshow=SimpleUploadedFile('My Presentation.key',
                                         'binary data'
                                         )
        )

    def create_slide(self, talk=None, number=None):
        """
        Utility function for creating slides.
        """

        return Slide.objects.create(
            talk=talk or self.talk_one,
            number=number,
            image=SimpleUploadedFile('Slide 1.png',
                                     'binary data'
                                     )
        )

    def test_create(self):
        """
        Create a slide, and test that the number of slides in the database is
        1, and that the unicode function correclty returns the word 'Slide' and
        the slide number.
        """

        self.create_slide()
        self.assertEqual(Slide.objects.count(), 1)
        self.assertEqual(unicode(Slide.objects.get()), u'Slide 1')

    def test_number_increment(self):
        """
        Create 3 slides, and test that the `number` field for each slide is
        correctly incremented, so that the first slide is numbered 1, the
        second 2 and the last one 3.
        """

        self.assertEqual(self.create_slide().number, 1)
        self.assertEqual(self.create_slide().number, 2)
        self.assertEqual(self.create_slide().number, 3)

    def test_unique_number_per_talk(self):
        """
        Create a slide for a talk, and test that an integrity error is raised
        when trying to create a slide with the same number, under the same
        talk.
        """

        self.create_slide(number=1)
        with self.assertRaises(IntegrityError):
            self.create_slide(number=1)

    def test_unique_number_talk_combo(self):
        """
        Create a slide, and test that a second slide can be created with the
        same number as the first, as long as they're under different talks.
        """

        self.create_slide(number=1)
        self.create_slide(self.talk_two, number=1)

    def test_update(self):
        """
        Update the created slide, and make sure that the returned number of
        updated rows is 1.
        """

        slide = self.create_slide()
        update = Slide.objects.filter(pk=slide.pk).update(
            notes='Now I have notes'
        )

        self.assertEqual(update, 1)

    def test_delete(self):
        """
        Delete a newly-created slide, and make sure the number of slides in the
        database is 0.
        """

        slide = self.create_slide()
        Slide.objects.get(pk=slide.pk).delete()
        self.assertEqual(Slide.objects.count(), 0)


class LinkTest(TestCase):
    """
    Tests for the `talks.Link` model
    """

    def setUp(self):
        """
        Create a talk that we can assign links to.
        """

        user, created = User.objects.get_or_create(username='foo')
        self.talk, created = Talk.objects.get_or_create(
            event=Event.objects.create(
                creator=user,
                name='DjangoCon EU 2016',
                slug='djangocon-eu-2016',
                date_from=date(2016, 3, 30),
                date_to=date(2016, 4, 1)
            ),
            title='10 Things I Hate About PHP',
            slug='10-things',
            creator=user,
            slideshow=SimpleUploadedFile('My Presentation.key',
                                         'binary data'
                                         )
        )

    def create_link(self):
        """
        Utility function for creating links.
        """

        return Link.objects.create(
            talk=self.talk,
            url='http://example.com',
            title='Example'
        )

    def test_create(self):
        """
        Create a link, and test that the number of links in the database is
        1, and that the unicode function correclty returns the link title.
        """

        self.create_link()
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(unicode(Link.objects.get()), u'Example')

    def test_update(self):
        """
        Update the created link, and make sure that the returned number of
        updated rows is 1.
        """

        link = self.create_link()
        update = Link.objects.filter(pk=link.pk).update(
            title='Example Link'
        )

        self.assertEqual(update, 1)

    def test_delete(self):
        """
        Delete a newly-created link, and make sure the number of links in the
        database is 0.
        """

        link = self.create_link()
        Link.objects.get(pk=link.pk).delete()
        self.assertEqual(Link.objects.count(), 0)

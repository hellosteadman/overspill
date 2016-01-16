from time import time
from os import path


def unique_id():
    """
    Returns a unique ID (a hex representation of the current UNIX timestamp)
    """
    return hex(int(time() * 10000000))[2:]


def set_talk_slideshow_url(talk, filename):
    """
    Returns the final path for the uploaded presentation file. Given a
    username of 'joe', a UNIX timestamp of 1452898693 and a file called
    talk.pptx, the filename for a talk added for an event whose ID is 1
    should be 'events/1/talks/joe_339e0960e8b080.pttx'.
    """

    return u'events/%d/talks/%s_%s%s' % (
        talk.event.pk,
        talk.creator.username,
        unique_id(),
        path.splitext(filename)[-1]
    )


def set_slide_image_url(slide, filename):
    """
    Returns the final path for the uploaded slide image. The third slide
    added for the second ever talk given at the first uploaded event should
    have a URL of 'events/1/talks/slides/2_3.png', given a PNG image.
    """

    return u'events/%d/talks/slides/%d_%d%s' % (
        slide.talk.event.pk,
        slide.talk.pk,
        slide.number,
        path.splitext(filename)[-1]
    )


def set_slide_audio_url(slide, filename):
    """
    Returns the final path for the slide's associated audio track. The
    third slide added for the second ever talk given at the first uploaded
    event should have a URL of 'events/1/talks/slides/2_3.mp3', given an
    MP3 audio file.
    """

    return u'events/%d/talks/slides/%d_%d%s' % (
        slide.talk.event.pk,
        slide.talk.pk,
        slide.number,
        path.splitext(filename)[-1]
    )

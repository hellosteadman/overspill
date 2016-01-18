from __future__ import absolute_import
from os import path, remove
from mimetypes import guess_type
from django.test import TestCase
from . import convert_to


class ConvertToTest(TestCase):
    def test_convert_key_to_png(self):
        # Load up our test Keynote file
        source = path.join(
                           path.dirname(__file__),
                           'fixtures',
                           'presentation.key'
                           )

        filename = convert_to(source, '.png')
        mimetype, encoding = guess_type(filename)

        # Check that the file we get back is a Zip
        self.assertEqual(mimetype, 'application/zip')

        # Delete the test file
        remove(filename)

    def test_convert_pptx_to_png(self):
        # Load up our test PowerPoint file
        source = path.join(
                           path.dirname(__file__),
                           'fixtures',
                           'presentation.pptx'
                           )

        filename = convert_to(source, '.png')
        mimetype, encoding = guess_type(filename)

        # Check that the file we get back is a Zip
        self.assertEqual(mimetype, 'application/zip')

        # Delete the test file
        remove(filename)

from __future__ import absolute_import
from os import path, write, close
from tempfile import mkstemp
from mimetypes import guess_type
import requests
from . import defaults


def convert_to(source, output_extension):
    """
    Given a source file, this will trigger a conversion via the CloudConvert
    API
    """

    # Ask to start a conversion,
    payload = {
        'apikey': defaults.API_KEY,
        'inputformat': path.splitext(source)[-1][1:],
        'outputformat': output_extension[1:]
    }

    # Parse the response.
    response = requests.post(defaults.START_PROCESS_URL, data=payload)
    if response.status_code == 200:
        json = response.json()
        url = json['url']
    else:
        response.raise_for_status()

    # Looks like we're good to go. Pass the conversion info to the URL we were
    # given.
    mimetype, encoding = guess_type(source)
    payload = {
        'input': 'upload',
        'outputformat': output_extension[1:],
        'wait': True,
        'download': True
    }

    files = [
        (
            'file',
            (
                path.split(source)[-1],
                open(source, 'rb'),
                mimetype
            )
        )
    ]

    response = requests.post('https:%s' % url, data=payload, files=files)
    if response.status_code == 200:
        handle, dest_filename = mkstemp('.zip')

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                write(handle, chunk)

        close(handle)
        return dest_filename
    else:
        response.raise_for_status()

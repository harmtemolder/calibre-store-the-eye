#!/usr/bin/env python3

"""A Python class to handle searching in, and downloading from, The
Eye's open directory. Technically it is not limited to e-books, but that
is what I will use it for.
"""

from bs4 import BeautifulSoup
from datetime import datetime
from functools import partial
import gzip
import itertools
import json
import os
from urllib.request import urlopen, Request

from calibre.constants import numeric_version
from calibre.devices.usbms.driver import debug_print as root_debug_print
from calibre.gui2 import error_dialog, warning_dialog, info_dialog
from calibre.utils.config import config_dir

DEFAULT_BASE_URL = 'https://the-eye.eu/public/Books/Calibre_Libraries/'
DEFAULT_INDEX_FILE = os.path.join(config_dir, 'plugins', 'The Eye.json.gz')

if numeric_version >= (5, 5, 0):
    module_debug_print = partial(root_debug_print, ' the_eye:main:', sep='')
else:
    module_debug_print = partial(root_debug_print, 'the_eye:main:')

class TheEye:
    def __init__(self, base_url=DEFAULT_BASE_URL,
                 index_file=DEFAULT_INDEX_FILE):

        self.base_url = base_url
        self.index_file = index_file
        self.load_index()

    def load_index(self):
        """Try to load a local index from a JSON file.
        """
        debug_print = partial(module_debug_print, 'TheEye:load_index:')

        if os.path.isfile(self.index_file):
            try:
                with gzip.open(self.index_file, mode='rt',
                               encoding='UTF-8') as json_gzip:
                    self.index = json.load(json_gzip)
            except Exception as e:
                debug_print('could not load index because of ', e)
                error_dialog(
                    None,
                    'Could not load The Eye index',
                    'Could not load The Eye index from {}'.format(
                        self.index_file),
                    det_msg=e,
                    show=True
                )
            else:
                debug_print('loaded index from {}'.format(self.index_file))
        else:
            debug_print('index file does not exist at {}'.format(
                self.index_file))
            error_dialog(
                None,
                'No The Eye index file found',
                'No The Eye index file found at {}. Please go to this '
                'plugin’s configuration and click “Update Index”.'.format(
                    self.index_file),
                show=True
            )


    def _get_links(self, url):
        """Request a URL and parse hrefs from the result.

        :param url: str pointing to a page within The Eye's /public/
        :return: list of hrefs on the page, from within <pre> tags
        """
        debug_print = partial(module_debug_print, 'TheEye:_crawl_links:')

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHT' \
                     'ML, like Gecko) Chrome/83.0.4086.0 Safari/537.36'

        try:
            r = urlopen(Request(url, headers={'User-agent': user_agent}))
            soup = BeautifulSoup(r.read(), 'html.parser')
            r.close()
        except Exception as e:
            debug_print('could not open {} because {}. Skipping...'.format(
                url, e))
            return []

        pre = soup.find('pre')

        if pre is None:  # i.e. empty dir
            return []

        anchors = pre.find_all('a')

        # Create a list of absolute URLs from the hrefs
        hrefs = [(url + a['href']) for a in anchors]

        # Drop the first href, since that points to the parent directory
        return hrefs[1:]

    def _crawl_links(self, url):
        """Gets all links from a page, then gets all links from the
        pages those links point to, etc.

        :param url: str pointing to a page to start crawling from
        :return: list of URLs of files (i.e. URLs not ending in '/')
        """
        debug_print = partial(module_debug_print, 'TheEye:_crawl_links:')
        debug_print('crawling {}'.format(url))

        links = self._get_links(url)

        pages = [l for l in links if l[-1] == '/']
        files = [l for l in links if l[-1] != '/']

        if len(pages) == 0:
            return files

        files = files + list(itertools.chain.from_iterable(
            [self._crawl_links(p) for p in pages]))

        return files

    def refresh_index(self, config, show_progress):
        """To be able to search within the directory with any reasonable
        speed, we need to keep a local index. To be compatible with
        calibre, this index is stored in a JSON file. This function
        refreshes that local index.
        """
        debug_print = partial(module_debug_print, 'TheEye:refresh_index:')

        debug_print('refreshing index from {}'.format(self.base_url))
        self.index = self._crawl_links(self.base_url)

        debug_print('compressing index into {}'.format(self.index_file))
        with gzip.open(self.index_file, mode='wb') as json_gzip:
            json_gzip.write(json.dumps(self.index, indent=4).encode())

        debug_print('writing `last_update` to config file')
        config['last_update'] = datetime.now().timestamp()
        config.commit()

    def search(self, query, mode='all', format='ALL'):
        """Search the index for any or all words in the given query
        (split on spaces), ignoring case. Returns a list of matching items

        :param query: str of keywords, space-separated
        :param mode: one of 'any' or 'all', whether all words should be
                     present to match. Defaults to 'all'
        :return: list of matching items
        """
        debug_print = partial(module_debug_print, 'TheEye:search:')

        if self.index is None:
            debug_print('cannot search without an index')
            return False

        query_split = query.decode().lower().split(' ')
        format_split = [f.strip() for f in format.lower().split(',')]

        if mode == 'any':
            matches = [i for i in self.index if
                any([q in i.lower() for q in query_split])]
        else:
            matches = [i for i in self.index if
                all([q in i.lower() for q in query_split])]

        if format.lower() != 'all':
            matches = [m for m in matches if
                m.split('.')[-1].lower() in format_split]

        debug_print('found {} match(es) for {}'.format(len(matches), query))
        return matches

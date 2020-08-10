#!/usr/bin/env python2

"""A Python class to handle searching in, and downloading from, The
Eye's open directory. Technically it is not limited to e-books, but that
is what I will use it for.
"""

import itertools
import json
import os
# import pickle
import urllib2

from bs4 import BeautifulSoup

class TheEye:
    def __init__(self,
                 base_url='https://the-eye.eu/public/Books/Calibre_Libraries/',
                 index_file='./the_eye.json'):
        print('the_eye.py:TheEye:__init__: begin')

        self.base_url = base_url
        self.index_file = index_file
        self.load_index()

        print('the_eye.py:TheEye:__init__: complete')

    def load_index(self):
        """Tries to load a local index from a JSON file. Creates a new
        file and index if there is none.

        :return: the index as a list of URLs pointing to files
        """
        print('the_eye.py:TheEye:load_index')

        if os.path.isfile(self.index_file):
            with open(self.index_file, mode='rb') as index_json:
                self.index = json.load(index_json)
        else:
            self.refresh_index()

            with open(self.index_file, mode='wb') as index_json:
               index_json.write(json.dumps(self.index, indent=4))

        print('the_eye.py:TheEye:load_index: len(self.index) =', str(len(self.index)))

        # return self.index

    def _get_links(self, url):
        """Requests a URL and parses hrefs from the result.

        :param url: str pointing to a page within The Eye's /public/
        :return: list of hrefs on the page, within <pre>
        """
        print('the_eye.py:TheEye:_get_links: url =', url)

        r = urllib2.urlopen(urllib2.Request(
            url,
            headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/'
                                  '537.36 (KHTML, like Gecko) Chrome/83.0.4086.'
                                  '0 Safari/537.36'}
        ))

        # While developing I used a stored response instead of
        # constantly querying The Eye
        # r = pickle.load(open('r.pkl', mode='rb'))
        # pickle.dump(r, open('./r.pkl', mode='wb'))

        soup = BeautifulSoup(r.read(), 'html.parser')
        r.close()

        pre = soup.find('pre')

        if pre is None:  # i.e. empty dir
            return []

        anchors = pre.find_all('a')

        # Create a list of absolute URLs from the hrefs
        hrefs = [(url + a['href'].encode('utf-8')) for a in anchors]

        # Drop the first href, since that points to the parent directory
        return hrefs[1:]

    def _crawl_links(self, url):
        """Gets all links from a page, then gets all links from the
        pages those links point to, etc.

        :param url: str pointing to a page to start crawling from
        :return: list of URLs of files (i.e. URLs not ending in '/')
        """
        print('the_eye.py:TheEye:_crawl_links: url =', url)

        links = self._get_links(url)

        pages = [l for l in links if l[-1] == '/']
        files = [l for l in links if l[-1] != '/']

        if len(pages) == 0:
            return files

        files = files + list(itertools.chain.from_iterable([
            self._crawl_links(p) for p in pages[0:2]]))  # TODO remove cap

        return files

    def refresh_index(self):
        """To be able to search within the directory with any reasonable
        speed, we need to keep a local index. To be compatible with
        Calibre, this index needs to be stored in a JSON file. This
        function refreshes that local index.

        :return: the index, loaded as one-dimensional list of URLs of
                 files
        """
        print('the_eye.py:TheEye:refresh_index')

        self.index = self._crawl_links(self.base_url)

        # with open(self.index_file, mode='wb') as index_json: TODO
        #     index_json.write(json.dumps(self.index, indent=4))

        # return self.index

    def search(self, query, mode='all'):
        """Search the index for any or all words in the given query
        (split on spaces), ignoring case. Returns a list of matching items

        :param query: str of keywords, space-separated
        :param mode: one of 'any' or 'all', whether all words should be
                     present to match. Defaults to 'all'
        :return: list of matching items
        """
        print('the_eye.py:TheEye:search: query =', query)

        keywords = query.split(' ')

        if mode == 'any':
            matches = [
                i for i in self.index
                if any([
                    k.lower() in i.lower() for k in keywords
                ])
            ]
        else:
            matches = [
                i for i in self.index
                if all([
                    k.lower() in i.lower() for k in keywords
                ])
            ]

        return matches


if __name__ == '__main__':
    eye = TheEye('https://the-eye.eu/public/Books/Calibre_Libraries/')

    # Make sure to refresh the index after changing the base URL
    # eye.refresh_index()

    print('\n'.join(eye.search('gandhi biography')))

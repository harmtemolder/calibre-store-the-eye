#!/usr/bin/env python2
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import urlparse

from calibre.customize import StoreBase
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.utils.config import config_dir

from .the_eye import TheEye

__license__ = 'GNU GPLv3'
__copyright__ = '2020, harmtemolder <mail at harmtemolder.com>'
__docformat__ = 'restructuredtext en'

class TheEyeStorePlugin(StorePlugin):
    def genesis(self):
        # print('TheEyeStorePlugin:genesis: Initializing self.eye')
        self.eye = TheEye(
            base_url='https://the-eye.eu/public/Books/Calibre_Libraries/',
            index_file=os.path.join(config_dir, 'plugins', 'The Eye.json'))

    def search(self, query, max_results=10, timeout=60):
        search_results = self.eye.search(query)

        for result in search_results[0:max_results]:
            parsed = urlparse.unquote(result)

            # print('TheEyeStorePlugin:search: parsed =', parsed)

            filename = parsed.split('/')[-1]
            stem = '.'.join(filename.split('.')[0:-1])
            extension = filename.split('.')[-1]

            s = SearchResult()
            s.title = stem
            s.author = ''
            s.price = '0.00'
            s.drm = SearchResult.DRM_UNLOCKED
            s.formats = extension.upper()
            s.downloads[extension.upper()] = result

            # print('TheEyeStorePlugin:search: s =', s, sep='\n')

            yield s

    def open(self, parent=None, detail_item=None, external=False):
        pass

class TheEyeStore(StoreBase):
    name = 'The Eye'
    description = 'Access The Eye directly from calibre.'
    version = (0, 1, 0)
    author = 'harmtemolder'
    drm_free_only = True

    def load_actual_plugin(self, gui):
        self.actual_plugin_object  = TheEyeStorePlugin(gui, self.name)
        return self.actual_plugin_object

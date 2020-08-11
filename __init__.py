#!/usr/bin/env python2

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import urlparse

from calibre.customize import StoreBase
from calibre.devices.usbms.driver import debug_print
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog
from calibre.utils.config import config_dir
from PyQt5.Qt import QUrl

from .the_eye import TheEye
from .config import TheEyeStoreConfig

__license__ = 'GNU GPLv3'
__copyright__ = '2020, harmtemolder <mail at harmtemolder.com>'
__docformat__ = 'restructuredtext en'

class TheEyeStorePlugin(TheEyeStoreConfig, StorePlugin):
    def initialize(self):
        """Called once when calibre plugins are initialized. Plugins are
        re-initialized every time a new plugin is added.

        :return: None
        """
        debug_print('The Eye::__init__.py:initialize:locals() =', locals())

        self.eye = TheEye(
            base_url='https://the-eye.eu/public/Books/Calibre_Libraries/',
            index_file=os.path.join(config_dir, 'plugins', 'The Eye.json.gz'))

        debug_print('The Eye::__init__.py:initialize:len(self.eye.index) =',
                    len(self.eye.index))

    def genesis(self):
        """Plugin specific initialization.

        :return: None
        """
        debug_print('The Eye::__init__.py:genesis:locals() =', locals())

        if not hasattr(self, 'eye'):  # i.e. not initialized by initialize()
            self.eye = TheEye(
                base_url='https://the-eye.eu/public/Books/Calibre_Libraries/',
                index_file=os.path.join(config_dir, 'plugins', 'The Eye.json.gz'))

            debug_print('The Eye::__init__.py:genesis:len(self.eye.index) =',
                        len(self.eye.index))

    def update_cache(self, parent=None, timeout=60, force=False,
                     suppress_progress=True):
        """

        :param parent:
        :param timeout:
        :param force:
        :param suppress_progress:
        :return: None
        """
        debug_print('The Eye::__init__.py:update_cache:locals() =', locals())

        self.eye.refresh_index()  # TODO


    def search(self, query, max_results=10, timeout=60):
        """A generator that yields SearchResult objects. It searches
        self.eye.index for matches containing all keywords.

        :param query:
        :param max_results:
        :param timeout:
        :yield: a SearchResult object
        """
        debug_print('The Eye::__init__.py:search:locals() =', locals())

        # Defaults to EPUBs containing all keywords
        search_results = self.eye.search(
            query, mode='all', format='EPUB')

        for result in search_results[0:max_results]:
            parsed = urlparse.unquote(result)

            debug_print('The Eye::__init__.py:search:parsed =', parsed)

            filename = parsed.split('/')[-1]
            stem = '.'.join(filename.split('.')[0:-1])
            extension = filename.split('.')[-1]

            s = SearchResult()
            s.title = stem
            s.author = ''
            s.price = '0.00'
            s.detail_item = result
            s.drm = SearchResult.DRM_UNLOCKED
            s.formats = extension.upper()
            s.downloads[extension.upper()] = result

            yield s

    def open(self, parent=None, detail_item=None, external=False):
        debug_print('The Eye::__init__.py:open:locals() =', locals())

        parent_url = '/'.join(detail_item.split('/')[0:-1])

        if external or self.config.get('open_external', False):
            open_url(QUrl(parent_url))
        else:
            d = WebStoreDialog(
                self.gui, self.eye.base_url, parent, parent_url)
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get('tags', ''))
            d.exec_()

class TheEyeStore(StoreBase):
    name = 'The Eye'
    description = 'Access The Eye directly from calibre.'
    version = (0, 1, 0)
    author = 'harmtemolder'
    drm_free_only = True

    def load_actual_plugin(self, gui):
        self.actual_plugin_object  = TheEyeStorePlugin(gui, self.name)
        return self.actual_plugin_object

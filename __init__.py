#!/usr/bin/env python2

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime
import os
import urlparse

from calibre.customize import StoreBase
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog
from calibre.utils.config import config_dir, JSONConfig
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
        self.eye = TheEye(
            base_url='https://the-eye.eu/public/Books/Calibre_Libraries/',
            index_file=os.path.join(config_dir, 'plugins/The Eye.json.gz'))

    def genesis(self):
        """Plugin specific initialization.

        :return: None
        """
        if not hasattr(self, 'eye'):  # i.e. not initialized by initialize()
            self.eye = TheEye(
                base_url='https://the-eye.eu/public/Books/Calibre_Libraries/',
                index_file=os.path.join(config_dir, 'plugins', 'The Eye.json.gz'))

    def update_cache(self, parent=None, timeout=60, force=False,
                     suppress_progress=True):
        """

        :param parent:
        :param timeout:
        :param force:
        :param suppress_progress:
        :return: None
        """
        if not hasattr(self, 'eye'):  # i.e. not initialized by initialize()
            self.eye = TheEye(
                base_url='https://the-eye.eu/public/Books/Calibre_Libraries/',
                index_file=os.path.join(config_dir, 'plugins', 'The Eye.json.gz'))

        self.eye.refresh_index()
        self.config['last_update'] = datetime.now()
        self.config.commit()

    def search(self, query, max_results=10, timeout=60):
        """A generator that yields SearchResult objects. It searches
        self.eye.index for matches containing all keywords.

        :param query:
        :param max_results:
        :param timeout:
        :yield: a SearchResult object
        """
        search_mode = ('all' if self.config.get('mode_all', True) else 'any')
        search_format = self.config.get('format', '')

        search_results = self.eye.search(
            query,
            mode=search_mode,
            format=('ALL' if search_format == '' else search_format))

        for result in search_results[0:max_results]:
            parsed = urlparse.unquote(result)

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
    config = JSONConfig('plugins/The Eye.json')

    def load_actual_plugin(self, gui):
        self.actual_plugin_object = TheEyeStorePlugin(
            gui, self.name, self.config)
        return self.actual_plugin_object

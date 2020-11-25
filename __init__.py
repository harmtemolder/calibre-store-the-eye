#!/usr/bin/env python3

from functools import partial
import os
import sys
from urllib.parse import unquote

from calibre.constants import DEBUG, numeric_version
from calibre.customize import StoreBase
from calibre.devices.usbms.driver import debug_print as root_debug_print
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog
from calibre.utils.config import JSONConfig
from PyQt5.Qt import QUrl

from calibre_plugins.the_eye.main import TheEye
from calibre_plugins.the_eye.config import TheEyeStoreConfig

if numeric_version >= (5, 5, 0):
    module_debug_print = partial(root_debug_print, ' the_eye:__init__:', sep='')
else:
    module_debug_print = partial(root_debug_print, 'the_eye:__init__:')

__license__   = 'GNU GPLv3'
__copyright__ = '2020, harmtemolder <mail at harmtemolder.com>'
__docformat__ = 'restructuredtext en'

PYDEVD = True  # Used during debugging to connect to PyCharm’s remote debugging

if DEBUG and PYDEVD:
    try:
        sys.path.append('/Applications/PyCharm.app/Contents/debug-eggs/pydevd'
                        '-pycharm.egg')
        import pydevd_pycharm
        pydevd_pycharm.settrace(
            'localhost', stdoutToServer=True, stderrToServer=True,
            suspend=False)
    except Exception as e:
        module_debug_print('could not start pydevd_pycharm, e = ', e)


class TheEyeStorePlugin(TheEyeStoreConfig, StorePlugin):
    def initialize(self):
        """Called once when calibre plugins are initialized. Plugins are
        re-initialized every time a new plugin is added.

        :return: None
        """
        if not hasattr(self, 'eye'):
            self.eye = TheEye()

    def genesis(self):
        """Plugin specific initialization.

        :return: None
        """
        if not hasattr(self, 'eye'):
            self.eye = TheEye()

    def update_cache(self, parent=None, timeout=60, force=False,
                     suppress_progress=True):
        """

        :param parent:
        :param timeout:
        :param force:
        :param suppress_progress:
        :return: None
        """
        if not hasattr(self, 'eye'):
            self.eye = TheEye()

        self.eye.refresh_index(self.config)

    def search(self, query, max_results=10, timeout=60):
        """A generator that yields SearchResult objects. It searches
        self.eye.index for matches containing all keywords.

        :param query:
        :param max_results:
        :param timeout:
        :yield: a SearchResult object
        """
        if not hasattr(self, 'eye'):
            self.eye = TheEye()

        search_mode = ('all' if self.config.get('mode_all', True) else 'any')
        search_format = self.config.get('format', '')

        search_results = self.eye.search(
            query,
            mode=search_mode,
            format=('ALL' if search_format == '' else search_format))

        for result in search_results[0:max_results]:
            parsed = unquote(result)

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
    name                    = 'The Eye'
    description             = 'Access The Eye directly from calibre.'
    author                  = 'harmtemolder'
    version                 = (0, 2, 1)
    minimum_calibre_version = (5, 0, 1)  # Because Python 3
    drm_free_only           = True
    config                  = JSONConfig(os.path.join('plugins', 'The Eye.json'))

    def load_actual_plugin(self, gui):
        self.actual_plugin_object = TheEyeStorePlugin(
            gui, self.name, self.config)
        return self.actual_plugin_object

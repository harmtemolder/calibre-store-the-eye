#!/usr/bin/env python2

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from calibre.ebooks.metadata.sources.update import debug_print
from calibre.gui2.store.basic_config import (BasicStoreConfigWidget,
                                             BasicStoreConfig)
from polyglot.builtins import unicode_type

class TheEyeStoreConfigWidget(BasicStoreConfigWidget):
    def load_setings(self):
        debug_print('The Eye::config.py:TheEyeStoreConfigWidget:load_setings:lo'
                    'cals() =',
                    locals())
        config = self.store.config

        self.open_external.setChecked(config.get('open_external', False))
        self.tags.setText(config.get('tags', ''))

class TheEyeStoreConfig(BasicStoreConfig):
    """This class contains all customization of The Eye store and should
    be inherited from by a TheEyeStorePlugin class.

    """

    # def is_customizable(self):
    #     """This method must return True to enable customization via
    #     Preferences->Plugins. Found it in "Find Duplicates".
    #     """
    #     return True

    def config_widget(self):
        """See :class:`calibre.customize.Plugin` for details.

        :return: a TheEyeStoreConfigWidget object
        """
        debug_print('The Eye::config.py:TheEyeStoreConfig:config_widget:locals('
                    ') =', locals())

        return TheEyeStoreConfigWidget(self)

    def save_settings(self, config_widget):
        """See :class:`calibre.customize.Plugin` for details.

        :return: None
        """
        debug_print('The Eye::config.py:TheEyeStoreConfig:save_settings:locals('
                    ') =', locals())

        self.config['open_external'] = config_widget.open_external.isChecked()
        tags = unicode_type(config_widget.tags.text())
        self.config['tags'] = tags


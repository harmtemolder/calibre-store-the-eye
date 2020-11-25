#!/usr/bin/env python3

from datetime import datetime
from functools import partial

from calibre.constants import numeric_version
from calibre.devices.usbms.driver import debug_print as root_debug_print
from calibre.gui2.store.basic_config import BasicStoreConfig
from polyglot.builtins import unicode_type
from PyQt5.Qt import (
    QCheckBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QVBoxLayout
)


if numeric_version >= (5, 5, 0):
    module_debug_print = partial(root_debug_print, ' the_eye:config:', sep='')
else:
    module_debug_print = partial(root_debug_print, 'the_eye:config:')


class TheEyeStoreConfigWidget(QWidget):
    def __init__(self, plugin):
        # Set up layout
        QWidget.__init__(self)
        debug_print = partial(module_debug_print, 'TheEyeStoreConfigWidget:__init__:')
        debug_print('start')
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set up Options group within layout
        options_group_box = QGroupBox(self)
        options_group_box.setTitle('Options')
        layout.addWidget(options_group_box)
        options_group_box_layout = QVBoxLayout(options_group_box)

        # Add format text field to Options group
        format_label = QLabel('Enter your desired formats as a '
                              'comma-separated list. Leave empty for all file'
                              ' types.')
        options_group_box_layout.addWidget(format_label)
        self.format = QLineEdit()
        self.format.setObjectName('format')
        self.format.setPlaceholderText('ALL')
        options_group_box_layout.addWidget(self.format)

        # Add checkbox for 'all' to Options group
        self.mode_all = QCheckBox('Search results must contain all keywords ('
                                  'instead of any).')
        self.mode_all.setObjectName('mode_all')
        options_group_box_layout.addWidget(self.mode_all)

        # Load settings
        self.load_setings(plugin)

        # Add group with update index button to layout
        update_group_box = QGroupBox(self)
        update_group_box.setTitle('Update Index')
        layout.addWidget(update_group_box)
        update_group_box_layout = QVBoxLayout(update_group_box)

        last_update_str = datetime.fromtimestamp(self.last_update).strftime(
            '%Y-%m-%d')

        update_label = QLabel('This plugin stores an index of The Eye '
                              'locally. This has {}. If you cannot find any '
                              'books, or encounter 404 errors when trying to '
                              'download books, you might want to update the '
                              'index. Note that this will take several '
                              'minutes, depending on your internet '
                              'speed.'.format(
            ('never been done'
             if self.last_update < 946695600
             else 'last been updated on {}'.format(last_update_str))))

        update_label.setWordWrap(True)
        update_group_box_layout.addWidget(update_label)
        update_pushbutton = QPushButton('Update Index')
        update_pushbutton.clicked.connect(
            lambda: plugin.update_cache(
                timeout=300,
                force=True,
                suppress_progress=False))

        update_group_box_layout.addWidget(update_pushbutton)

        # Add group with text to layout
        issues_group_box = QGroupBox(self)
        issues_group_box.setTitle('Errors and Requests')
        layout.addWidget(issues_group_box)
        issues_group_box_layout = QVBoxLayout(issues_group_box)
        issues_label = QLabel('Please report any errors or requests on <a '
                              'href="https://github.com/harmtemolder/calibre'
                              '-store-the-eye/issues">this plugin\'s GitHub '
                              'repository page</a>.')
        issues_label.setOpenExternalLinks(True)
        issues_group_box_layout.addWidget(issues_label)

        self.setMinimumSize(self.sizeHint())

    def load_setings(self, plugin):
        debug_print = partial(
            module_debug_print, 'TheEyeStoreConfigWidget:load_setings:')

        config = plugin.config

        debug_print('config = ', config)

        self.format.setText(config.get('format', ''))
        self.mode_all.setChecked(config.get('mode_all', True))
        self.last_update = config.get('last_update', 0.0)


class TheEyeStoreConfig(BasicStoreConfig):
    """This class contains all customization of The Eye store and should
    be inherited from by a TheEyeStorePlugin class.

    """

    def config_widget(self):
        """See :class:`calibre.customize.Plugin` for details.

        :return: a TheEyeStoreConfigWidget object
        """
        return TheEyeStoreConfigWidget(self)

    def save_settings(self, config_widget):
        """See :class:`calibre.customize.Plugin` for details.

        :return: None
        """
        debug_print = partial(
            module_debug_print, 'TheEyeStoreConfigWidget:save_settings:')

        debug_print('vars(self) =', vars(self))

        self.config['mode_all'] = config_widget.mode_all.isChecked()
        self.config['format'] = unicode_type(config_widget.format.text())
        self.config.commit()

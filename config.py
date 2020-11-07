#!/usr/bin/env python3

from datetime import datetime

from calibre.ebooks.metadata.sources.update import debug_print
from calibre.gui2.store.basic_config import BasicStoreConfig
from polyglot.builtins import unicode_type
from PyQt5.Qt import (QCheckBox, QGridLayout, QGroupBox, QLabel, QLineEdit,
    QPushButton, QWidget, QVBoxLayout)


class TheEyeStoreConfigWidget(QWidget):
    def __init__(self, plugin):
        # Set up layout
        QWidget.__init__(self)
        self.l = QVBoxLayout()
        self.setLayout(self.l)

        # Set up Options group within layout
        options_group_box = QGroupBox(self)
        options_group_box.setTitle(_('Options'))
        self.l.addWidget(options_group_box)
        options_group_box_layout = QGridLayout(options_group_box)

        # Add format text field to Options group
        format_label = QLabel(_('Enter your desired formats as a comma-separate'
                                'd list. Leave empty for all file types.'))
        options_group_box_layout.addWidget(format_label)
        self.format = QLineEdit()
        self.format.setObjectName('format')
        self.format.setPlaceholderText('ALL')
        options_group_box_layout.addWidget(self.format)

        # Add checkbox for 'all' to Options group
        self.mode_all = QCheckBox(_('Search results must contain all keywords ('
                                    'instead of any).'))
        self.mode_all.setObjectName('mode_all')
        options_group_box_layout.addWidget(self.mode_all)

        # Load settings
        self.load_setings(plugin)

        # Add group with update index button to layout
        update_group_box = QGroupBox(self)
        update_group_box.setTitle(_('Update Index'))
        self.l.addWidget(update_group_box)
        update_group_box_layout = QGridLayout(update_group_box)

        update_label = QLabel(_('This plugin stores an index of The Eye locally'
                                '. This has {}. If you encounter 404 errors whe'
                                'n trying to download books, you might want to '
                                'update the index.'.format((
            'never been done' if self.last_update < datetime(
                2000, 1, 1) else 'last been updated on {}'.format(
                    self.last_update.strftime('%Y-%m-%d'))))))

        update_group_box_layout.addWidget(update_label)
        update_pushbutton = QPushButton(_('Update Index'))
        update_pushbutton.clicked.connect(
            lambda:plugin.update_cache(
                timeout=300,
                force=True,
                suppress_progress=False))

        update_group_box_layout.addWidget(update_pushbutton)

        # Add group with text to layout
        issues_group_box = QGroupBox(self)
        issues_group_box.setTitle(_('Errors and Requests'))
        self.l.addWidget(issues_group_box)
        issues_group_box_layout = QGridLayout(issues_group_box)
        issues_label = QLabel(_('Please report any errors or requests on <a hre'
                                'f="https://github.com/harmtemolder/calibre-sto'
                                're-the-eye/issues">this plugin\'s GitHub repos'
                                'itory page</a>.'))
        issues_label.setOpenExternalLinks(True)
        issues_group_box_layout.addWidget(issues_label)

    def load_setings(self, plugin):
        config = plugin.config

        debug_print('The Eye::config.py:TheEyeStoreConfigWidget:load_setings:co'
                    'nfig =', config)

        self.format.setText(config.get('format', ''))
        self.mode_all.setChecked(config.get('mode_all', True))
        self.last_update = config.get('last_update', datetime.fromtimestamp(0))


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
        debug_print('The Eye::config.py:TheEyeStoreConfig:save_settings:vars('
                    'self) =', vars(self))

        self.config['mode_all'] = config_widget.mode_all.isChecked()
        self.config['format'] = unicode_type(config_widget.format.text())
        self.config.commit()


if __name__ == '__main__':
    from calibre.gui2 import Application
    from calibre.gui2.preferences import test_widget

    app = Application([])
    test_widget('Advanced', 'Plugins')

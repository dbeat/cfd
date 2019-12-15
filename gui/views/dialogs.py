# -*- coding: utf-8 -*-
"""
gui.view.dialogs.py
October 10, 2019
@author: Francois Roy
"""
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDialog, QLabel, QVBoxLayout, QPushButton, QProgressBar)
# from PyQt5.QtWebKitWidgets import QWebView  # if pyqt5 < 5.6
from PyQt5.QtWebEngineWidgets import QWebEngineView

from gui.resources import documentation_icon, help_icon
from utils import ROOT_DIR

DOCUMENTATION_DIR = ROOT_DIR


class DocumentationDialog(QDialog):
    r"""The documentation dialog."""

    def __init__(self, parent=None):
        """
        Display a dialog that shows the package documentation.
        """
        super(DocumentationDialog, self).__init__(parent)
        self.setWindowTitle('Documentation')
        self.setWindowIcon(QIcon(documentation_icon))
        self.resize(1250, 800)
        self.layout = QVBoxLayout()


class AboutDialog(QDialog):
    r"""The about dialog."""

    def __init__(self, parent=None):
        """Display a dialog that shows application information."""
        super(AboutDialog, self).__init__(parent)

        self.setWindowTitle('About')
        self.setWindowIcon(QIcon(help_icon))
        self.resize(300, 200)

        author = QLabel('Nucleus Scientific Inc.')
        author.setAlignment(Qt.AlignCenter)

        icons = QLabel('Test Bench')
        icons.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)

        self.layout.addWidget(author)
        self.layout.addWidget(icons)

        self.setLayout(self.layout)

# -*- coding: utf-8 -*-
"""
gui.view.console_view.py
October 10, 2019
@author: Francois Roy
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont, QColor

from ..resources import DEBUG, ERROR, INFO, WARNING


class ConsoleView(QTextEdit):
    r"""Overwrite QTextEdit to display logs in different colors."""
    def __init__(self, parent=None):
        super(ConsoleView, self).__init__(parent)
        self.setReadOnly(True)
        self.font = QFont()
        self.font.ExtraBold

    def display(self, text, color=Qt.black):
        r"""Display logs in text edit field.

        :param text: The test to be displayed.
        :param color:
        :type text: str
        """
        # self.clear()
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)

        blue = QColor('dodgerBlue')
        green = QColor('green')
        orange = QColor('darkOrange')  # from x11 color database
        red = QColor('red')

        if 'Dummy' in text:
            text = text.replace('Dummy', 'Qt_threadpool')

        char_format = cursor.charFormat()
        char_format.setFont(self.font)
        char_format.setFontWeight(QFont.Normal)
        if DEBUG.upper() in text:
            char_format.setForeground(blue)
        elif INFO.upper() in text:
            char_format.setForeground(green)
        elif WARNING.upper() in text:
            char_format.setForeground(orange)        
        elif ERROR.upper() in text:
            char_format.setForeground(red)
            char_format.setFontWeight(QFont.Bold)
        else:
            char_format.setForeground(color)
            char_format.setFontWeight(QFont.Normal)

        cursor.setCharFormat(char_format)
        cursor.insertText(text)
        cursor.movePosition(cursor.End)
        self.ensureCursorVisible()

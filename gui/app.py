# -*- coding: utf-8 -*-
"""
gui.app.py
October 10, 2019
@author: Francois Roy
"""
import sys
import threading

from PyQt5.QtCore import (QSize, Qt, QModelIndex)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QDockWidget, QProgressBar, QAction,
                             QToolBar)

from .resources import (results_icon, exit_icon,
                        documentation_icon, clear_console_icon, help_icon,
                        show_icon)
from .views.console_view import ConsoleView
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from .views.central_view import CentralView
from fem import *
from utils import APP_DIR
import traceback
import vtk
from .tree import Tree
from .views.tree_view import TreeView

# /usr/lib/x86_64-linux-gnu/qt5/bin/designer
LOGGER_FORMAT = "%(asctime)s - [%(levelname)s] (%qthreadName)s): %(message)s\n"


def trap_exc_during_debug(*args):
    r"""when app raises uncaught exception, print error on console.
    exc_type, exc_obj, exc_tb = sys.exc_info()
    args are defined in the Worker class
    """
    logging.error('{} {}\n      Stack traceback:{}'.format(
        args[0],
        args[1],
        traceback.extract_tb(args[2])),
                  extra={'qthreadName': threading.current_thread().name})


# install exception hook: without this, uncaught exception would cause
# application to exit
sys.excepthook = trap_exc_during_debug


class QtHandler(logging.Handler):
    r"""Send logs to the console widget."""
    def __init__(self, parent):
        super(QtHandler, self).__init__()
        self.widget = ConsoleView(parent)

    def emit(self, record):
        msg = self.format(record)
        self.widget.display(msg)


class App(QMainWindow):
    r"""The application."""
    def __init__(self, parent=None, app=None):
        super(App, self).__init__(parent)
        self.app = app
        screen_resolution = app.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.resize(width-200, height-200)  # 1024 x 768

        self.setWindowTitle('MOTOR')
        self.setWindowIcon(QIcon(results_icon))

        # console view
        log_text_box = QtHandler(self)
        f = LOGGER_FORMAT
        self.extra = {'qthreadName': threading.current_thread().name}
        log_text_box.setFormatter(logging.Formatter(f))
        logging.getLogger().addHandler(log_text_box)
        logging.getLogger().setLevel(logging.DEBUG)
        self.console = QDockWidget("Console", self)
        self.console.setWidget(log_text_box.widget)
        self.console.setFloating(False)
        # self.console.setMinimumSize(QSize(1024, 200))
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console)

        # status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready', 5000)
        self.progressBar = QProgressBar()
        # Places the progress bar right aligned with addPermanentWidget
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.hide()

        # initialize model
        self._model = Tree('t')

        # display view
        self.display_dock = QDockWidget("Data Display", self)
        self.display_widget = QVTKRenderWindowInteractor()
        self.display_dock.setWidget(self.display_widget)
        self.display_widget.setMinimumSize(QSize(width/2, height/2))
        self.display_dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.display_dock)
        # The source file
        file_name = APP_DIR.child("triangle_mesh_linear.vtu")
        # file_name = "m_fix_geometry.vtk"

        # Read the source file.
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(file_name)
        reader.Update()  # Needed because of GetScalarRange
        output = reader.GetOutput()
        # scalar_range = output.GetScalarRange()

        pressure = output.GetPointData().GetArray("pressure")
        velocity = output.GetPointData().GetArray("velocity")
        # print(pressure.GetValue(6))
        # print(velocity.GetValue(12))

        # Create the mapper that corresponds the objects of the vtk.vtk file
        # into graphics elements
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(output)
        # mapper.SetScalarRange(scalar_range)
        mapper.ScalarVisibilityOff()

        # Create the Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().SetLineWidth(2.0)

        colors = vtk.vtkNamedColors()
        backface = vtk.vtkProperty()
        backface.SetColor(colors.GetColor3d("tomato"))
        actor.SetBackfaceProperty(backface)

        # Create the Renderer
        renderer = vtk.vtkRenderer()
        renderer.AddActor(actor)
        renderer.SetBackground(1, 1, 1)  # Set background to white
        renderer.SetBackground(colors.GetColor3d("Wheat"))

        # Create the RendererWindowInteractor and display the vtk_file
        self.interactor = self.display_widget.GetRenderWindow().GetInteractor()
        # Create the RendererWindow
        renderer_window = self.display_widget.GetRenderWindow()
        renderer_window.AddRenderer(renderer)

        self.show()
        self.interactor.Initialize()
        self.interactor.Start()

        # central view
        self.central_view = CentralView(parent=self)
        self.central_view.setMinimumSize(QSize(700, 400))
        self.setCentralWidget(self.central_view)
        # set initial selection for root index
        self.central_view.set_selection(QModelIndex())
        # set model
        # self.central_view.set_model(self._model)

        self.tree_dock = QDockWidget("Model Tree", self)
        self.tree_widget = TreeView(self._model)
        self.tree_view = self.tree_widget.tree_view
        self.tree_dock.setWidget(self.tree_widget)
        self.tree_dock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.tree_dock)

        # tool bar
        self.tool_bar_items()
        self.tool_bar = None

        # menu bar
        self.menu_bar = self.menuBar()
        if os.name == 'posix':  # mac
            self.menu_bar.setNativeMenuBar(False)
        # self.about_dialog = AboutDialog()
        # self.documentation_dialog = DocumentationDialog(self)
        self.file_menu()
        self.help_menu()

        # initialize actions
        self.file_sub_menu = None
        self.help_sub_menu = None
        self.restore_action = None
        self.exit_action = None
        self.about_action = None
        self.documentation_action = None

    def file_menu(self):
        r"""Create a file submenu with an Open File item that opens a file
        dialog.
        """
        self.file_sub_menu = self.menu_bar.addMenu('File')

        self.restore_action = QAction(QIcon(show_icon), 'Show All Widgets',
                                      self)
        self.restore_action.setStatusTip('Show all widgets.')
        self.restore_action.setShortcut('CTRL+R')
        self.restore_action.triggered.connect(self.restore_desktop)

        self.exit_action = QAction(QIcon(exit_icon), 'Exit Application', self)
        self.exit_action.setStatusTip('Exit the application.')
        self.exit_action.setShortcut('CTRL+Q')
        # TODO: Make sure all devices are closed
        self.exit_action.triggered.connect(lambda: QApplication.quit())

        self.file_sub_menu.addAction(self.restore_action)
        self.file_sub_menu.addAction(self.exit_action)

    def help_menu(self):
        r"""Create a help submenu with an About item tha opens an about dialog.
        """
        self.help_sub_menu = self.menu_bar.addMenu('Help')
        self.about_action = QAction(QIcon(help_icon), 'About', self)
        self.about_action.setStatusTip('About the application.')
        self.about_action.setShortcut('CTRL+H')
        self.about_action.triggered.connect(
            lambda: self.about_dialog.exec_())

        self.documentation_action = QAction(QIcon(documentation_icon),
                                            'Documentation', self)
        self.documentation_action.setStatusTip('Access online documentation.')
        self.documentation_action.setShortcut('CTRL+D')
        self.documentation_action.triggered.connect(
            lambda: self.documentation_dialog.exec_())

        self.help_sub_menu.addAction(self.about_action)
        self.help_sub_menu.addAction(self.documentation_action)

    def tool_bar_items(self):
        r"""Create a tool bar for the main window.
        """
        self.tool_bar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)
        self.tool_bar.setMovable(False)
        tool_bar_clear_console_action = QAction(QIcon(clear_console_icon),
                                                'Clear console', self)
        tool_bar_clear_console_action.triggered.connect(self.clear_console)
        self.tool_bar.addAction(tool_bar_clear_console_action)

    def restore_desktop(self):
        r"""Show docked items.
        """
        self.display_dock.setVisible(True)
        self.console.setVisible(True)

    def clear_console(self):
        r"""Open the calculator in a dialog
        """
        self.console.widget().clear()

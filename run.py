# -*- coding: utf-8 -*-
"""
run.py
November 14, 2019
@author Francois Roy
"""
import sys
import click
import traceback
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from gui.app import App

from fem import *
from resources import __application__, __version__
from cfd.models_2d.axi_symmetric.poiseuille_axi import *


def print_version(ctx, param, value):
    r"""Prints the version and exits the program in the callback.

    :param param:
    :param ctx: Click internal object that holds state relevant for the script
      execution.
    :param value: Close the program without printing the version if False.
    :type ctx: click.context
    :type value: bool
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo('{} {} (Python {})'.format(
        __application__,
        __version__,
        sys.version[:3]
    ))
    ctx.exit()


@click.command()
@click.option('-g', '--gui', is_flag=True,
              help="Start the graphical user interface.")
@click.option('-r', '--run', is_flag=True,
              help="Run the batch job and exit.")
@click.option(
    '-v', '--version',
    is_flag=True, help='Show version information and exit.',
    callback=print_version, expose_value=False, is_eager=True,
)
def main(gui, run):
    r"""CFD: A user interface to solve CFD problems using FEniCS
    """
    if gui:
        pass
        # application = QApplication(sys.argv)
        # application.setStyle("cleanLooks")
        # try:
        #    # TODO: check os and pass the name to application
        #    window = App(app=application)
        #    desktop = QDesktopWidget().availableGeometry()
        #    width = (desktop.width() - window.width()) / 2
        #    height = (desktop.height() - window.height()) / 2
        #    window.show()
        #    window.move(width, height)
        #    sys.exit(application.exec_())
        # except Exception as exc:
        #    print(exc)
        #    traceback.print_tb(sys.exc_info()[2])
    elif run:
        # define batch job here
        # model list with parameters
        # the run option launch a basic gui showing statistics, log and status.
        # selected results are saved on file at each time steps, the job can
        # be stopped and resumed at anytime, starting from the last
        # saved solution.
        models = [PoiseuilleAxi('pa1')]
        for m in models:
            m.compute()
            # p, uz = model.exact_solution()
            # print(p)
            # print(uz)

    else:
        pass


if __name__ == '__main__':
    main()

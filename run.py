# -*- coding: utf-8 -*-
"""
run.py
November 14, 2019
@author Francois Roy
"""
import sys
import click
import traceback

from utils import logging
from resources import __application__, __version__
from cfd.models_2d.axi_symmetric.poiseuille_axi import *
from cfd.models_2d.poiseuille_plane import *
from fem import *


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
@click.option('-d', '--db', is_flag=True,
              help="Show models database interface.")
@click.option('-r', '--run', is_flag=True,
              help="Run the batch job and exit.")
@click.option(
    '-v', '--version',
    is_flag=True, help='Show version information and exit.',
    callback=print_version, expose_value=False, is_eager=True,
)
def main(db, run):
    r"""Run a batch job, show status and log, solve results to file after
    each time step, write report to file and save file in MongoDB database.

    The database GUI can be accessed after the job has ran, using the
    ``db`` option.
    """
    if db:
        # launch the db interface in the default browser. Load new models
        # stats and results into the database if exists.
        # show model list, add model, edit/remove model, compare models
        logging.info("Not implemented yet.")
    elif run:
        # define batch job here
        # model list with parameters
        # the run option launch a basic gui showing statistics, log and status.
        # selected results are saved on file at each time steps, the job can
        # be stopped and resumed at anytime, starting from the last
        # saved solution.
        models = [PoiseuillePlane()]  # PoiseuilleAxi('pa1')]
        for model in models:
            model.compute()
            # p, uz = model.exact_solution()
            # print(p)
            # print(uz)

    else:
        pass


if __name__ == '__main__':

    main()

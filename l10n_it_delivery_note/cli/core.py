# Copyright (c) 2020, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import argparse
import functools
import logging
import odoo

from odoo import SUPERUSER_ID
from odoo.cli import Command

_logger = logging.getLogger(__name__)


def environment(funct=None, parser_args_method=None):
    if not funct:
        return functools.partial(environment,
                                 parser_args_method=parser_args_method)

    @functools.wraps(funct)
    def env_enabler(self, args):
        command_args = unknown_args = args

        if parser_args_method:
            command_args, unknown_args = parser_args_method(self, args)

        odoo.tools.config._parse_config(unknown_args)
        odoo.netsvc.init_logger()

        config = odoo.tools.config

        with odoo.api.Environment.manage():
            cr = odoo.registry(config['db_name']).cursor()
            env = odoo.api.Environment(cr, SUPERUSER_ID, {})

            funct(self, command_args, env)

    return env_enabler


class EasyCommand(Command):
    args = None
    env = None

    is_debugging = None

    def __init__(self):
        self.is_debugging = False

    def _commit(self):
        self.env.cr.commit()  # pylint: disable=invalid-commit

    def _rollback(self):
        self.env.cr.rollback()

    def _close(self):
        self.env.cr.close()

    def initialize(self, args, env):
        self.args = args
        self.env = env

        if args:
            self.is_debugging = args.debug

    def execute(self):
        raise NotImplementedError("This method hasn't yet been implemented.")

    # noinspection PyMethodMayBeStatic
    def get_args_parser(self):
        args_parser = argparse.ArgumentParser()
        args_parser.add_argument('--debug', action='store_true', default=False)

        return args_parser

    def parse_args(self, args):
        arg_parser = self.get_args_parser()

        return arg_parser.parse_known_args(args)

    @environment(parser_args_method=parse_args)
    def run(self, args, env):
        try:
            self.initialize(args, env)
            self.execute()

            _logger.info("Execution completed successfully! Committing...")

            self._commit()

        except:
            _logger.exception("Something went wrong during command execution. "
                              "Rolling back...")

            self._rollback()

        finally:
            self._close()

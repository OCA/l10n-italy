#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Pylint disabled because relative might be
# from ... import hooks
# but it raises
# > ImportError: attempted relative import with no known parent package
# pylint: disable=odoo-addons-relative-import
from . import hooks


def migrate(cr, installed_version):
    # Used by OpenUpgrade when module is in `apriori`
    hooks.migrate_old_module(cr)

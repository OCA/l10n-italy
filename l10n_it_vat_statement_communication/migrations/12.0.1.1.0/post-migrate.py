#
# Copyright (c) 2019, Link IT srl, Italy. All rights reserved.
#

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        _logger.warning("""
            There is no previous version of the module.
            Skip the migration.
            """)

        return

    _logger.info("Set the default value on the new company field.")
    cr.execute("""
        UPDATE res_company
        SET vsc_supply_code = 'IVP18';
    """)

    _logger.info("Migration terminated.")

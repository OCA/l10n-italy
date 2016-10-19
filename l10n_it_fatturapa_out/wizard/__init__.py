# -*- coding: utf-8 -*-
# Copyright (C) 2014 Davide Corio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)

# there are multiple statements that should be guarded
# in wizard_export_fatturapa, so we guard the entire file
try:
    from . import wizard_export_fatturapa
except ImportError:
    _logger.debug('Cannot `import pyxb`.')  # Avoid init error if not installed

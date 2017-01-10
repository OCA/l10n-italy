# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging

_logger = logging.getLogger(__name__)

# pyxb is referenced in several in top-level statements in
# fatturapa_v_1_2, so we guard the import of the entire file
try:
    from . import fatturapa_v_1_2
except ImportError:
    _logger.debug('Cannot `import pyxb`.')  # Avoid init error if not installed

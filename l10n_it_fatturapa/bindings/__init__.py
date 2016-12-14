# -*- coding: utf-8 -*-
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

_logger = logging.getLogger(__name__)

# pyxb is referenced in several in top-level statements in
# fatturapa_v_1_1, so we guard the import of the entire file
try:
    from . import fatturapa_v_1_1
except ImportError:
    _logger.debug('Cannot `import pyxb`.')  # Avoid init error if not installed

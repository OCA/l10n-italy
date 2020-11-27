# -*- coding: utf-8 -*-
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group

# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

_logger = logging.getLogger(__name__)

try:
    import pyxb
except ImportError as e:
    _logger.warning(e)
else:
    try:
        from . import fatturapa  # noqa: F401
    except pyxb.PyXBVersionError as e:
        _logger.warning('%s: %s' % (e.__class__.__name__, e))

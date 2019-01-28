import logging

_logger = logging.getLogger(__name__)

try:
    from . import fatturapa_v_1_2
except Exception as e:  # ImportError or pyxb.PyXBVersionError
    _logger.warning('%s: %s' % (e.__class__.__name__, e))

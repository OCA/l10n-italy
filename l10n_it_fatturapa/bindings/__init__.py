import logging

_logger = logging.getLogger(__name__)

try:
    import pyxb
except ImportError as e:
    _logger.warning(e)
else:
    pyxb.PreserveInputTimeZone(True)
    try:
        from . import fatturapa_v_1_2
    except pyxb.PyXBVersionError as e:
        _logger.warning('%s: %s' % (e.__class__.__name__, e))

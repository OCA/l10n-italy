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

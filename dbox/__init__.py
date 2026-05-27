import logging

__version__ = "{{VERSION}}"
__commit_id__ = "{{COMMIT_ID}}"

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.info("version=%s commit_id=%s", __version__, __commit_id__)

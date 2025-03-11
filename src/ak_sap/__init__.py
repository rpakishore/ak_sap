"""
.. include:: ../../README.md
"""

from ak_sap.misc import Coord as Coord
from ak_sap.utils.logger import log
from ak_sap.wrapper import Sap2000Wrapper as Sap2000Wrapper


def debug(status: bool = False):
    """Set the logging level to DEBUG."""
    if status:
        log.setLevel(10)  # debug
    else:
        log.setLevel(20)  # info


debug(status=False)

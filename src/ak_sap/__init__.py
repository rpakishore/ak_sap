"Python wrapper for SAP2000 API"
__version__ = "0.0.4"

from ak_sap.misc import Coord
from ak_sap.utils.logger import log
from ak_sap.wrapper import Sap2000Wrapper


def debug(status=False):
    """Import this in a new module and enable debug to use debug
    example:
    ```python
    from ak_sap import debug
    debug(True)
    ```
    """
    if status:
        log.setLevel(10)  # debug
    else:
        log.setLevel(20)  # info


debug(status=False)

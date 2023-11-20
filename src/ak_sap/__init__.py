"Python wrapper for SAP2000 API"
__version__ = "0.0.1"

from ak_sap.utils.logger import log, ic
from ak_sap.wrapper import Sap2000Wrapper

#log = Log()

def debug(status=False):
    """Import this in a new module and enable debug to use debug
    example:
    ```python
    from ak_sap import debug
    debug(True)
    ```
    """
    if status:
        ic.enable()
        log.setLevel(10) #debug
    else:
        ic.disable()
        log.setLevel(20) #info

    log.debug(f'Icecream Debugger: {ic.enabled}')
    
debug(status=False)
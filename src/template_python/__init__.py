"Placeholder module info"
__version__ = "0.0.1"

from template_python.logger import Log
from icecream import ic

log = Log()
log.info('Template Module Initialized')

def debug(status=False):
    """Import this in a new module and enable debug to use debug
    example:
    ```python
    from template_python import debug
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
import sys
from pathlib import Path
import getpass
from . import log, ic
ic.configureOutput(prefix=f'{Path(__file__).name} -> ')

if sys.platform=="win32":
    import keyring, getpass


def getpwd(item, username):
    if sys.platform=="win32":
        log.debug(f'getting pwd for `{username}` in `{item}`')
        pwd = keyring.get_password(item, username)
        if not pwd:
            log.warning("Password is not saved in keyring.")
            pwd = getpass.getpass(f"Enter the password for {item} corresponding to Username:{username}: ")
    else:
        pwd = getpass.getpass(f"Enter the password for `{item}` corresponding to Username:`{username}`  : ")
    
    return pwd
import getpass
from pathlib import Path
import sys

from . import log

if sys.platform=="win32":
    import getpass
    import keyring


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
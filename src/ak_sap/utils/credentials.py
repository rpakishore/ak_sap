import getpass
import keyring

from . import log

def getpwd(item, username):
    log.debug(f'getting pwd for `{username}` in `{item}`')
    pwd = keyring.get_password(item, username)
    if not pwd:
        log.warning("Password is not saved in keyring.")
        pwd = getpass.getpass(f"Enter the password for {item} corresponding to Username:{username}: ")
    return pwd
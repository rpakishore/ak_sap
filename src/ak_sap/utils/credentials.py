import getpass

import keyring

from . import log


def getpwd(item, username):
    """Retrieves a password stored in the keyring.

    If the password is not found in the keyring, prompts the user to
    enter it manually.

    Args:
        item (str): The item for which to retrieve the password.
        username (str): The username associated with the password.

    Returns:
        str: The retrieved password.
    """
    log.debug(f"getting pwd for `{username}` in `{item}`")
    pwd = keyring.get_password(item, username)
    if not pwd:
        log.warning("Password is not saved in keyring.")
        pwd = getpass.getpass(
            f"Enter the password for {item} corresponding to Username:{username}: "
        )
    return pwd

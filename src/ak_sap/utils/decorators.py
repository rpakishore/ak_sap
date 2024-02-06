from ak_sap import log
from functools import wraps

def smooth_sap_do(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            if isinstance(ret, list) or isinstance(ret, tuple):
                assert ret[-1] == 0, f'{ret=} indicates failure to complete command'
                return ret[0]
            else:
                assert ret == 0, f'{ret=} indicates failure to complete command'
                return ret
        except Exception as e:
            log.critical(e)
    return wrapper
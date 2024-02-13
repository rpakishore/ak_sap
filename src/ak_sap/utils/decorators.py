from ak_sap import log
from functools import wraps

def smooth_sap_do(func):
    """Wrapper for running SAP OAPI calls. 
    Will check for return response from SAP. 
    If not '0' will log and exit gracefully."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.debug(f'Running `{func.__qualname__}` with args: "{args}" and kwargs: "{kwargs}"')
            ret = func(*args, **kwargs)
            log.debug(f'Response received: {ret}')
            if isinstance(ret, list) or isinstance(ret, tuple):
                assert ret[-1] == 0, f'{ret=} indicates failure to complete command'
                if len(ret) == 2:
                    return ret[0]
                return ret[:-1]
            else:
                assert ret == 0, f'{ret=} indicates failure to complete command'
                return ret
        except Exception as e:
            log.critical(e)
    return wrapper
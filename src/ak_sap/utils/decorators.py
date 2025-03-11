from functools import wraps

from ak_sap import log


def smooth_sap_do(func):
    """Decorator for running SAP API calls smoothly.

    This wrapper checks for the return response from SAP. If it does
    not return '0', it logs the error and exits gracefully.

    Args:
        func (callable): The function being decorated.

    Returns:
        callable: The wrapped function with error handling.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.debug(
                f'Running `{func.__qualname__}` with args: "{args}" and kwargs: "{kwargs}"'
            )
            ret = func(*args, **kwargs)
            log.debug(f"Response received: {ret}")
            if isinstance(ret, list) or isinstance(ret, tuple):
                assert ret[-1] == 0, f"{ret=} indicates failure to complete command"
                if len(ret) == 2:
                    return ret[0]
                return ret[:-1]
            else:
                assert ret == 0, f"{ret=} indicates failure to complete command"
                return ret
        except Exception as e:
            log.critical(e)

    return wrapper

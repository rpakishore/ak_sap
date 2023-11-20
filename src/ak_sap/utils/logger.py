from icecream import ic

import inspect
import logging
import getpass
from pathlib import Path
import time

class Log(object):
    #class CALog(logging.Logger):
# Reference - 
# http://yhhuang1966.blogspot.com/2018/04/python-logging_24.html
    def __init__(self):
        user=getpass.getuser()
        self.logger=logging.getLogger(user)
        self.logger.setLevel(logging.INFO)
        format='%(asctime)s-%(levelname)s: %(message)s'
        formatter=logging.Formatter(format, datefmt='%Y%m%d-%H%M%S')
        streamhandler=logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        self.logger.addHandler(streamhandler)
        log_dir: Path = Path(__file__).parent.parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        logfile = log_dir / f'{user}{time.strftime("-%Y-%b")}.log'
        filehandler=logging.FileHandler(logfile, encoding="utf-8")
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)
    def debug(self, msg):
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.info(msg)
    def warning(self, msg):
        try:
            suffix = f'Warning in {Path(inspect.stack()[1].filename).name} -> {inspect.currentframe().f_back.f_code.co_name}: '
        except Exception:
            suffix = f'Warning in {Path(inspect.stack()[1].filename).name}: '
        self.logger.warning(suffix + msg)
    def error(self, msg):
        try:
            suffix = f'Error in {Path(inspect.stack()[1].filename).name} -> {inspect.currentframe().f_back.f_code.co_name}: '
        except Exception:
            suffix = f'Error in {Path(inspect.stack()[1].filename).name}: '
        self.logger.error(suffix + msg)
    def critical(self, msg):
        try:
            suffix = f'Critical in {Path(inspect.stack()[1].filename).name} -> {inspect.currentframe().f_back.f_code.co_name}: '
        except Exception:
            suffix = f'Error in {Path(inspect.stack()[1].filename).name}: '
        self.logger.critical(suffix + msg)
    def log(self, level, msg):
        self.logger.log(level, msg)
    def setLevel(self, level):
        self.logger.setLevel(level)
    def disable(self):
        logging.disable(50)
        
log = Log()
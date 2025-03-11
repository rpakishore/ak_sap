"""Module providing enhanced logging functionality with stack trace information.

This module extends basic logging capabilities by adding stack trace information
to warning and error messages, and provides functionality to read log contents.
"""

import getpass
import inspect
import logging
import time
from pathlib import Path

from . import paths


class Log(object):
    """Enhanced logging class with stack trace information and log file reading capabilities.

    This class extends Python's logging functionality by automatically including
    file and function names in warning and error messages. It also provides
    methods to read the contents of log files.

    Attributes:
        logger (logging.Logger): The underlying logger instance configured with
            both stream and file handlers.
        logfile (Path): Path to the log file being used.

    Example:
        >>> log = Log()
        >>> log.info("Application started")
        >>> log.error("Database connection failed")  # Will include stack trace
        >>> recent_logs = log.contents(10)  # Get last 10 log entries
    """

    def __init__(self):
        """Initialize the logger with stream and file handlers.

        Sets up a logger instance with the current user's username and configures
        both console and file logging. The log files are stored in a 'logs'
        directory within the source directory. If handlers already exist for the
        logger, no new handlers are added to prevent duplicate logging.
        """
        user = getpass.getuser()
        self.logger = logging.getLogger(user)
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)
            format = "%(asctime)s-%(levelname)s: %(message)s"
            formatter = logging.Formatter(format, datefmt="%Y%m%d-%H%M%S")

            # Set up console handler
            streamhandler = logging.StreamHandler()
            streamhandler.setFormatter(formatter)
            self.logger.addHandler(streamhandler)

            # Set up file handler
            dir_logs: Path = paths.dir_src / "logs"
            dir_logs.mkdir(exist_ok=True)
            logfile = dir_logs / f"{user}{time.strftime('-%Y-%b')}.log"
            self.logfile = logfile
            filehandler = logging.FileHandler(logfile, encoding="utf-8")
            filehandler.setFormatter(formatter)
            self.logger.addHandler(filehandler)

    def debug(self, msg):
        """Log a debug message.

        Args:
            msg: The message to log at DEBUG level.
        """
        self.logger.debug(msg)

    def info(self, msg):
        """Log an info message.

        Args:
            msg: The message to log at INFO level.
        """
        self.logger.info(msg)

    def warning(self, msg):
        """Log a warning message with stack trace information.

        Prepends the warning message with the filename and function name where
        the warning was triggered.

        Args:
            msg: The message to log at WARNING level.
        """
        try:
            suffix = f"Warning in {Path(inspect.stack()[1].filename).name} -> {inspect.currentframe().f_back.f_code.co_name}: "
        except Exception:
            suffix = f"Warning in {Path(inspect.stack()[1].filename).name}: "
        self.logger.warning(suffix + msg)

    def error(self, msg):
        """Log an error message with stack trace information.

        Prepends the error message with the filename and function name where
        the error occurred. Also logs the full exception traceback.

        Args:
            msg: The message to log at ERROR level.
        """
        try:
            suffix = f"Error in {Path(inspect.stack()[1].filename).name} -> {inspect.currentframe().f_back.f_code.co_name}: "
        except Exception:
            suffix = f"Error in {Path(inspect.stack()[1].filename).name}: "
        self.logger.error(suffix + str(msg))
        self.logger.exception(msg)

    def critical(self, msg):
        """Log a critical message with stack trace information.

        Prepends the critical message with the filename and function name where
        the critical error occurred. Also logs the full exception traceback.

        Args:
            msg: The message to log at CRITICAL level.
        """
        try:
            suffix = f"Critical in {Path(inspect.stack()[1].filename).name} -> {inspect.currentframe().f_back.f_code.co_name}: "
        except Exception:
            suffix = f"Error in {Path(inspect.stack()[1].filename).name}: "
        self.logger.critical(suffix + str(msg))
        self.logger.exception(msg)

    def log(self, level, msg):
        """Log a message at a specified level.

        Args:
            level: The logging level to use (e.g., logging.INFO, logging.ERROR)
            msg: The message to log at the specified level.
        """
        self.logger.log(level, msg)

    def setLevel(self, level):
        """Set the minimum logging level for the logger.

        Args:
            level: The minimum logging level (e.g., logging.DEBUG, logging.INFO)
        """
        self.logger.setLevel(level)

    def disable(self):
        """Disable all logging.

        Disables all logging by setting the logging level to 50 (CRITICAL + 10),
        effectively preventing any messages from being logged.
        """
        logging.disable(50)

    def contents(self, lines: int = 9999) -> list[str]:
        """Read the most recent lines from the log file.

        Args:
            lines: Number of most recent lines to read from the log file.
                Defaults to 9999.

        Returns:
            list[str]: A list of the most recent log entries, with length
                limited by the lines parameter.
        """
        with open(self.logfile, "r") as f:
            data = f.readlines()
            _len = len(data)
            return data[_len - min(lines, _len) :]


# Create a global logger instance
log = Log()
"""Global logger instance"""

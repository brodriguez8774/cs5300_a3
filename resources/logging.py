"""
Logging initialization.
Note: Standard log priority is "NOTSET" > "DEBUG" > "INFO" > "WARNING" > "ERROR" > "CRITICAL".
"""

# System Imports.
import logging.config, os


def get_logger(caller):
    """
    Returns an instance of the logger. Always pass the __name__ attribute.
    By calling through here, guarantees that logger will always have proper settings loaded.
    :param caller: __name__ attribute of caller.
    :return: Instance of logger, associated with caller's __name__.
    """
    return logging.getLogger(caller)


# Find project_dir logging path.
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(project_dir, 'resources/logs')
if not os.path.exists(log_dir):
    print('Error initializing logging.')


# Define a new, "test result" log level.
# TESTRESULT = 5
# def testresult(self, message, *args, **kwargs):
#     self.log(TESTRESULT, message, *args, **kwargs)
# logging.Logger.testresult = testresult


def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Code directly imported from https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.
    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.
    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present
    Example
    -------
    >> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >> logging.getLogger(__name__).setLevel("TRACE")
    >> logging.getLogger(__name__).trace('that worked')
    >> logging.trace('so did this')
    >> logging.TRACE
    5
    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

addLoggingLevel('TESTRESULT', 55)


# Dictionary style logging options.
LOGGING = {
    'version': 1,
    'formatters': {
        # Message only logging. Only includes message.
        'message_only': {
            'format': '%(message)s',
        },
        # Simple logging. Includes message type and actual message.
        'simple': {
            'format': '[%(levelname)s]: %(message)s',
        },
        # Basic logging. Includes date, message type, file originated, and actual message.
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
        # Verbose logging. Includes standard plus the process number and thread id.
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s || %(process)d %(thread)d || %(message)s',
        },
    },
    'handlers': {
        # Sends log message to the void. May be useful for debugging.
        'null': {
            'class': 'logging.NullHandler',
        },
        # To console.
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Debug Level to file.
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, 'debug.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'standard',
        },
        # Info Level to file.
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, 'info.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'standard',
        },
        # Warn Level to file.
        'file_warn': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, 'warn.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        # TestResult Level  to file.
        'file_test_result': {
            'level': 'TESTRESULT',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, 'test_result.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'message_only',
        },
    },
    'loggers': {
        # All basic logging.
        '': {
            'handlers': ['console', 'file_debug', 'file_info', 'file_warn', 'file_test_result', ],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
}

# Load dictionary of settings into logger.
logging.config.dictConfig(LOGGING)

# Test logging.
logger = get_logger(__name__)
logger.info('Logging initialized.')
logger.info('Logging directory: ' + log_dir)

# # Test a "test_result" level log message.
# logger.testresult('Test Result level test.')

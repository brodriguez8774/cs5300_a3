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
    os.makedirs(log_dir)


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
    },
    'loggers': {
        # All basic logging.
        '': {
            'handlers': ['console', 'file_debug', 'file_info', 'file_warn', ],
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

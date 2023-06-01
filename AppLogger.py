import logging
import os

# Logging levels
# logging.debug - diagnosing problems
# .info         - things working as expected
# .warning      - something unexpected happened
# .error        - software unable to perform a function
# .critical     - software really in problem now

def init():
    path_to_log = os.getcwd()
    logging.basicConfig(filename=(path_to_log + '\\log\\log.txt'), encoding='utf-8',
            level=logging.DEBUG)
    
def log(msg):
    logging.warn(msg)

def log_debug(msg):
    logging.debug(msg)

def log_warning(msg):
    logging.warning(msg)

def log_error(msg):
    logging.error(msg)

def log_critical(msg):
    logging.critical(msg)

# TODO - create functions to log SQL queries

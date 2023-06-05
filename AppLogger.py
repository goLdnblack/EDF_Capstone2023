import logging
import os
from datetime import datetime

# Logging levels
# logging.debug - diagnosing problems
# .info         - things working as expected
# .warning      - something unexpected happened
# .error        - software unable to perform a function
# .critical     - software really in trouble now

def getTime():
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%m-%d-%Y %H:%M:%S")
    return timestamp

def init():
    path_to_log = os.getcwd()
    logging.basicConfig(filename=(path_to_log + '\\log\\log.txt'), encoding='utf-8',
            level=logging.DEBUG)
    logging.info(getTime() + " | Logger initiated.")
    
def log(msg):
    logging.warn(getTime() + " | " + msg)

def log_debug(msg):
    logging.debug(getTime() + " | " + msg)

def log_warning(msg):
    logging.warning(getTime() + " | " + msg)

def log_error(msg):
    logging.error(getTime() + " | " + msg)

def log_critical(msg):
    logging.critical(getTime() + " | " + msg)

# TODO - create functions to log SQL queries

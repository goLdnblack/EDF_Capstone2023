import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Logging levels
# logging.debug - diagnosing problems
# .info         - things working as expected
# .warning      - something unexpected happened
# .error        - software unable to perform a function
# .critical     - software really in trouble now

# Format options for logger
formatter = logging.Formatter('%(asctime)s - %(name)s Function: %(funcName)s | %(levelname)s | %(message)s', 
                              datefmt='%Y-%m-%d %H:%M:%S')

def getTime():
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%m-%d-%Y %H:%M:%S")
    return timestamp

def getTimeFileName():
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%m-%d-%Y_%H-%M")
    return timestamp

# Logger class
class LogApp(logging.Logger):
    def __init__(self, name, level = logging.DEBUG):
        # TODO - when creating logger class, also run setupLogger
        #setupLogger(name, log_file)
        return super(LogApp, self).__init__(name, level)
    
    def critical(self, msg, *args, **kwargs):
        # TODO - perform extra step on critical message
        #print('Send email')
        return super(LogApp, self).critical(msg, *args, **kwargs)
    

# Default level is WARNING
def setupLogger(name, log_dir, level=logging.DEBUG):
    handler = RotatingFileHandler(log_dir + '\\' + name + '_' + getTimeFileName() + '.log', 
                                  maxBytes=50*1000, backupCount=10)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.info('Logger initialized.')
    return logger

# TODO - create functions to log SQL queries

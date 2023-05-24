import logging
import os

loglevel={'info':logging.INFO, 'debug':logging.DEBUG}


def getLogger(name, level=None, applog=False):
    
    log_dir = "logMessage"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    format = logging.Formatter('[%(asctime)s] %(threadName)s %(levelname)s: %(message)s')
    
    console = logging.StreamHandler()
    console.setFormatter(format)
    
    handler = logging.FileHandler(log_dir + '/DistJET.' + name + '.log')
    handler.setFormatter(format)
    if not level:
        level = 'info'
            
    logger = logging.getLogger('DistJET.' + name)
    logger.setLevel(loglevel[level])
    logger.addHandler(handler)
    if console:
        print ("log %s add console handler"%name)
        logger.addHandler(console)
    return logger


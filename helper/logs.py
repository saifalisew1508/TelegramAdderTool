import logging
import sys
def log(name):
    # create logger Name PYRO
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
    # create console handler and set level to INFO
        pyro = logging.StreamHandler()
        pyro.setLevel(logging.INFO)
        
        # create formatter For PYRO
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        
        # add formatter to pyro
        pyro.setFormatter(formatter)
        
        # add ch to logger
        logger.addHandler(pyro)
    else:
        pass
    return logger

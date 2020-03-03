import os
import sys
import logging 

logger = logging.getLogger(__name__)

def exception():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

    message = " Error Type: " + str(exc_type) + " Error Message: " + str(exc_obj) + " Error occurred in file: " + str(
        fname) + " at line number: " + str(exc_tb.tb_lineno)
    return message

def log_exception():
    return logger.exception(exception())
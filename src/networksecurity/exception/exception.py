import os
import sys
from src.networksecurity.logging import logger
 

def error_message_details(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="error occured in the python script name [{0}] line number [{1}] error message[{2}]".format(file_name,exc_tb.tb_lineno,str(error))
    return error_message

class NetWorkSecurityException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_details(error_message,error_detail)

    def __str__(self):
        return self.error_message        


   # test the excption   file
"""
if __name__ == '__main__':
    try:
        logger.logging.info("enter the try block")
        a=1/0
    except Exception as e:
        
        raise NetWorkSecurityException(e,sys) """
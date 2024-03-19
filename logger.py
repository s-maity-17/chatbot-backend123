import sys
import logging

#from pytz import timezone 
#from datetime import datetime
#import json

#from inspect import getframeinfo, stack

class LOGGER:
    def __init__(self, ):
        '''
        self.styles = {
            'HINT': '\033[75m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m',
            'INFO': '\033[94m',
            'SUCCESS': '\033[92m',
            'WARNING': '\033[93m',
            'ERROR': '\033[91m',
            'END': '\033[0m'
        }
        '''

        self.args = {}
        self.kwargs = {}

        logger = logging.getLogger("connector-service")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(logging.Formatter(fmt='%(asctime)s | %(levelname)s | %(message)s'))
        logger.addHandler(handler)

        self.logger = logger

    '''
    def __print(self, ):
        date_time = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S')
        print(self.styles['BOLD'] + date_time + self.styles['END'], end='\t')

        print(self.styles[self.level] + self.level + self.styles['END'], end='\t')

        for arg in self.args:
            print(self.styles['BOLD'] + arg + self.styles['END'], end='\t')
        print()

        print(self.styles['UNDERLINE'] + 'Trace:' + self.styles['END'], end=' ')
        print(self.styles['HINT'] + json.dumps(self.kwargs, allow_nan = True) + self.styles['END'], end='\t')
        print()

        print(self.styles['UNDERLINE'] + 'Log:' + self.styles['END'], end=' ')
        log = {k:str(v) for k,v in self.log.items()}
        print(self.styles['HINT'] + json.dumps(log, allow_nan = True) + self.styles['END'], end='\t')
        print()

        print(self.styles['UNDERLINE'] + 'Code:' + self.styles['END'], end=' ')
        caller = getframeinfo(stack()[2][0])
        code = {}
        code['file_name'] = caller.filename
        code['line_no'] = caller.lineno
        code['function_name'] = caller.function
        print(self.styles['HINT'] + json.dumps(code, allow_nan = True) + self.styles['END'], end='\n')
    '''
    
    def base(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    
    def critical(self, log):
        self.logger.critical({**self.kwargs, **log})

    def error(self, log):
        self.logger.error({**self.kwargs, **log})

    def warning(self, log):
        self.logger.warning({**self.kwargs, **log})

    def info(self, log):
        self.logger.info({**self.kwargs, **log})

    def debug(self, log):
        self.logger.debug({**self.kwargs, **log})

Logger = LOGGER()
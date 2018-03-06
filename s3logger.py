import smart_open
from datetime import datetime, timedelta
from logging import Handler


import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

def _clean_s3_path(path):
    if path.endswith('/'):
        return path[:-1]
    return path


        
class S3LogHandler(Handler):
    """Pretty much copied from my colleagues code 
       https://github.com/fbertsch/s3_stream_logger/edit/master/logger.py

       Example
       -------
       import logging
       from s3logger import S3LogHandler
       logger = logging.getLogger('myapp')
       hdlr = S3LogHandler(bucket="mozilla-metrics",
                           prefix="user/sguha/tmp",
                           contextId = '12812ldqu3e')
       formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
       hdlr.setFormatter(formatter)
       logger.addHandler(hdlr) 
       logger.setLevel(logging.INFO)
       logger.info("FOO")

    """

    _buffer_size = 5 * 1024 ** 2

    def __init__(self, bucket, prefix, contextId):
        Handler.__init__(self)
        self.bucket = _clean_s3_path(bucket)
        self.prefix = _clean_s3_path(prefix)
        self.ctxid = _clean_s3_path(contextId)
        self.conn = S3Connection() 
        self.c = boto.connect_s3()
        self.b = self.c.get_bucket(self.bucket)
        self.k = Key(self.b)
        self.k.key = '{}/{}/logfile.txt'.format(self.prefix,self.ctxid)
        with open('/tmp/frobbish','w') as f:
            f.write("")
        

    def emit(self, record):
        log_entry = self.format(record)
        with open("/tmp/frobbish","r") as f:
            e = f.read()
        e = '{}{}\n'.format(e,log_entry)
        self.k.set_contents_from_string(e)
        with open("/tmp/frobbish","a+") as f:
            f.write(log_entry+"\n")

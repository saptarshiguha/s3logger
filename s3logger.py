import smart_open
from datetime import datetime, timedelta
from logging import Handler

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
        self.filename = 's3://{}/{}/{}/logfile.txt'.format(self.bucket, self.prefix, self.ctxid)


    def emit(self, record):
        log_entry = self.format(record)
        with smart_open.smart_open(self.filename, "r") as f:
            content = f.read()
        self.file = smart_open.smart_open(self.filename, 'w')
        self.file.write(content+log_entry + '\n')
        self.file.close()

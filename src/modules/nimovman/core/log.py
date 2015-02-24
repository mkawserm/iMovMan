'''
Created on Aug 8, 2013

@author: KaWsEr
'''



import os
import sys
import config
import inspect
import traceback
import logging.handlers
import logging

def whosdaddy():
    return inspect.stack()[2][3]
def caller_name(skip=1):
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]
    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        # be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>': # top level usually
        name.append( codename ) # function or a method
    del parentframe
    return ".".join(name)

#print caller_name()




####################################################
def error():
    """TraceBack Error"""
    for frame in traceback.extract_tb(sys.exc_info()[2]):
        fname,lineno,fn,text = frame
        estr="[%s:%d] - Error:%s" % ("function ("+fn+") :: "+fname,lineno,text)
        #print estr
        return estr
##########################################




##########################################


"""
class Log(object):
    def __init__(self,name):self.name=name
    def debug(self,*kwards,**kwargs):
        logger = logging.getLogger(self.name)
        try:logger.debug(*kwards,**kwargs)
        except:pass
    def error(self,*kwards,**kwargs):
        logger = logging.getLogger(self.name)
        try:logger.error(*kwards,**kwargs)
        except:pass
    def info(self,*kwards,**kwargs):
        logger = logging.getLogger(self.name)
        try:logger.info(*kwards,**kwargs)
        except:pass
    def critical(self,*kwards,**kwargs):
        logger = logging.getLogger(self.name)
        try:logger.critical(*kwards,**kwargs)
        except:pass

    def Instance(self):return self
"""










#@util.onlyone


class Log(object):
    def make_dirs(self,p):
        dn=os.path.dirname(p)
        if dn!="":
            if not os.path.exists(dn):
                os.makedirs(dn)
    def __init__(self,name):
        # create logger
        #logging.basicConfig(filename=os.path.join(util.getAppPath(),"iMovMan.log"),level=logging.DEBUG)
        formatter = logging.Formatter('%(name)s : [%(levelname)s] : %(asctime)s : %(message)s')
        formatter.datefmt="%Y-%m-%d %H:%M:%S"
        # create file handler which logs even debug messages
        fname=config.LOG_FILE
        #self.fh = logging.FileHandler(fname)
        #self.fh.setLevel(logging.DEBUG)
        if not os.path.exists(fname):
            self.make_dirs(fname)
            
        
        

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            # create console handler with a higher log level
            ch = logging.StreamHandler()
            #self.ch.setLevel(logging.ERROR)
            ch.setLevel(logging.DEBUG)
            # create formatter and add it to the handlers
            ch.setFormatter(formatter)
            #self.fh.setFormatter(formatter)
            # add the handlers to logger
            
            handler = logging.handlers.RotatingFileHandler(fname, maxBytes=1024*1024*1, backupCount=1)
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            # create the handlers and call logger.addHandler(logging_handler)
            self.logger.addHandler(ch)
            #self.logger.addHandler(self.fh)
            self.logger.addHandler(handler)
        
    def debug(self,*kwards,**kwargs):
        #self.logger = logging.getLogger(name)
        try:self.logger.debug(*kwards,**kwargs)
        except:pass
        #print caller_name()
        #print whosdaddy()
    def error(self,*kwards,**kwargs):
        #self.logger = logging.getLogger(name)
        try:self.logger.error(*kwards,**kwargs)
        except:pass
        #self.logger.error()
    def info(self,*kwards,**kwargs):
        #self.logger = logging.getLogger(name)
        try:self.logger.info(*kwards,**kwargs)
        except:pass
    def critical(self,*kwards,**kwargs):
        #self.logger = logging.getLogger(name)
        try:self.logger.critical(*kwards,**kwargs)
        except:pass

    def Instance(self):return self
    
    
'''
Created on May 17, 2013

@author: KaWsEr
'''
import os
import ast
import threading
from PySide.QtCore import QObject
from PySide.QtCore import Signal
import idb
import config
#import time




class MySignal(QObject):
    sig = Signal(str)

####Crawl File From Hrad Disk
class FileCrawler(threading.Thread):
    def __init__(self,obj_mainwindow):
        threading.Thread.__init__(self)
        self.__lock=threading.Lock()#thread safe lock, help to write and read
        self.daemon=True
        self.signal = MySignal()
        self.reset(obj_mainwindow)
        
    def reset(self,obj_mainwindow):
        """Reset All Things when necessary"""
        with self.__lock:
            self.idb=idb.IDb()
            self.cdb=idb.CDb()
            self.mainwindow=obj_mainwindow
            self.__TH={}
            self.path=[]
            self.__name="File Crawler"
            self.setName(self.__name)
            
            self.__is_running=False#state of running
            
            self._stop=threading.Event()
            self.__aam=0
            self.__iam=0
            self.__tcm=0
            self.__error=0
            self.__elist=[]
            
            #print self.mf
            #self.path=cnf["movie_path"]
            #print cnf
            #print self.cdb.has_key("movie_format")
            #if self.cdb.has_key("movie_path"):
            #    self.path=self.cdb.get("movie_path").value
            
            
            self.one=True
            #print self.path
            
    def stop(self):
        for sk in self.__TH.keys():
            if self.__TH[sk].isAlive():
                self.__TH[sk].join()
        self._stop.set()
    
    def stopped(self):
        return self._stop.isSet()
    
    def isRunning(self):
        """Return the running state of it"""
        return self.__is_running
    
    
    def crawl_file(self,lpath):
        with self.__lock:
            #print self.path
            for spath in lpath:
                if os.path.exists(spath):
                    for (path,dirs, files) in os.walk(spath):
                        #print dirs
                        dirs
                        #print "Found  : ",dirs
                        for s_file in files:
                            movie_path=os.path.realpath(os.path.join(path, s_file))
                            for single_format in self.mf:
                                if movie_path.lower().endswith(single_format.lower()):
                                    self.mainwindow.scanner.setText(os.path.basename(movie_path))
                                    try:
                                        #midb=idb.IDb()
                                        self.idb.add(movie_path)
                                    except Exception,e:
                                        print e
                                        self.mainwindow.scanner.setText(str(e))
                                    
                                    #time.sleep(1)
    def nonthreaded(self):
        try:
            mcdb=idb.CDb()
            cnf=mcdb.all()
            self.mf=ast.literal_eval(cnf["movie_format"])
            self.path=ast.literal_eval(cnf["movie_path"])
        except:
            self.path=[]
            self.mf=config.C_MOVIE_FORMAT
        try:
            
            self.crawl_file(self.path)
        except Exception,e:print e
    
    def crawl(self):self.nonthreaded()
        
    def run(self):
        #counter=0
        #self.mainwindow.show_spin()
        self.__is_running=True
        while not self.stopped():
            self.nonthreaded()
            #midb=idb.IDb()
            self.idb.trash_manager()
            if self.one:
                self.__is_running=False
                break
        #self.mainwindow.spinner.stop()
        self.mainwindow.scanner.setText("Done.")
        self.signal.sig.emit('')
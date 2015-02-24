'''
Created on Aug 14, 2013

@author: KaWsEr
'''

from PySide.QtGui import QMenu,QAction,QIcon
#from PySide.QtCore import SIGNAL,SLOT
from PySide import QtGui,QtCore

from modules.nimovman.core.dbmodel import Option,Movie,Trash
from modules.nimovman.core import Log,error
from modules.nimovman.core.config import appicon
from modules.nimovman.core.immjob import *
from modules.nimovman.core import util

import time
import threading
import trashwindow

class SendtoAction(QAction):
    def __init__(self,name,drive,parent):
        super(SendtoAction,self).__init__(name,parent)
        self.setIcon(QIcon(appicon("drive")))
        self.drive=drive


#Custom Signals#
class sigMoviesMenuMultipleDelete(QtCore.QObject):
    signal=QtCore.Signal(int)#1 Started #2finished
class sigMoviesMenuDeletedPath(QtCore.QObject):
    signal=QtCore.Signal(unicode)

class MoviesMenu(QMenu):
    MoviesMenuMultipleDeleteStatus=sigMoviesMenuMultipleDelete()
    MoviesMenuDeletedPath=sigMoviesMenuDeletedPath()
    
    def __init__(self,items,parent):
        self.__name="MoviesMenu"
        #self.vparent=parent
        super(MoviesMenu,self).__init__(parent)
        self.items=items
        self.drives=get_drives_details()
        self.send_to=self.drive_menu()
        delete=QAction(QIcon(appicon("delete")),"Delete",self )
        delete.setToolTip("Delete from database")
        delete.triggered.connect(self.click_event)
        #self.addAction(play)
        #self.addAction(delete)
        #self.addAction(edit)
        #self.addAction(update_imdbid)
        self.addSeparator()
        self.addAction(delete)
        self.addSeparator()
        #self.addAction(properties)
        self.addMenu(self.send_to)
        #self.connect(self, SIGNAL("triggered(QAction)"), self, SLOT("self.click_drive_menu(QAction*)"))
        #self.triggered.connect(self.click_drive_menu)
        
    
    def click_event(self):
        if type(self.sender())==QAction:
            act=self.sender().text().lower()
            
            
            if act=="delete":
                count=len(self.items)
                reply = QtGui.QMessageBox.question(self.parent(),
                                                   "Delete %s Movies?"%count,
                                                   "Are you sure to delete  %s movies from database?"%count,
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                
                if reply == QtGui.QMessageBox.Yes:
                    Log(self.__name).info("Delete initiating : %s",list(item.path for item in self.items) )
                    thr=threading.Thread(target=self.__delete_movies,args=())
                    thr.setDaemon(True)
                    thr.start()
                else:
                    Log(self.__name).info("Delete Cancelled : %s",list(item.path for item in self.items))
                #try:file_play(self.path)
                #except Exception,e:Log(self.__name).critical("%s %s",e,error())
                
        elif type(self.sender())==SendtoAction:
            print self.sender().drive



    def __delete_movies(self):
        #SimpleUi.update_signal.signal.emit("spin","start")
        MoviesMenu.MoviesMenuMultipleDeleteStatus.signal.emit(1)
        trash=Trash()
        movie=Movie()
        for item in self.items:
            try:
                tadd=trash.add(item.path)
                Log(self.__name).info("Trash Add %s: %s",item.path,tadd)
                mdel=movie.delete(item.path)
                Log(self.__name).info("Movie Delete %s: %s",item.path,mdel)
                MoviesMenu.MoviesMenuDeletedPath.signal.emit(item.path)
                time.sleep(0.5)
                trashwindow.TrashWindow.TrashDataReset.signal.emit(1)
            except Exception,e:
                Log(self.__name).critical("%s %s",e,error())
        MoviesMenu.MoviesMenuMultipleDeleteStatus.signal.emit(2)
        
    def drive_menu(self):
        send_to=QMenu("Send To")
        send_to.setIcon(QIcon(appicon("send_to")))
        for i in self.drives:
            if util.isWindows():
                k=SendtoAction("%s (%s)"%(i[1],i[0][0:2]),i[0],self)
                k.triggered.connect(self.click_event)
                #k.clicked.connect(self.click_drive_menu)
                send_to.addAction(k)
                
            elif util.isLinux():
                k=SendtoAction("%s"%(i[1]),i[0],self)
                k.triggered.connect(self.click_event)
                #k.clicked.connect(self.click_drive_menu)
                send_to.addAction(k)
                
        #send_to.triggered.connect(self.click_drive_menu)
        #send_to.
        
        
        return send_to
'''
Created on Aug 17, 2013

@author: KaWsEr
'''

import time
from PySide import QtGui
from PySide import QtCore
from modules.nimovman.core import standardsignal
from modules.nimovman.core import config

class ProgressBar(QtGui.QDialog):
    ProgressStarted=standardsignal.SignalInt()
    ProgressReport=standardsignal.SignalInt()
    ProgressFinished=standardsignal.SignalBool()
    ProgressMessage=standardsignal.SignalUnicode()
    def __init__(self):
        super(ProgressBar,self).__init__(None)
        self.setWindowIcon(QtGui.QIcon(config.appicon("iMovMan")))
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint )
        self.setModal(True)
        
        self.progress_bar=QtGui.QProgressBar(self)
        self.progress_bar.setFixedWidth(400)
        self.progress_bar.setMinimum(0)
        self.setFixedWidth(400)
        self.setFixedHeight(50)
        #TrashWindow.TotalTrashItems.signal.connect(self.total_trash_items)
        #TrashWindow.TotalTrashed.signal.connect(self.trashed)
        #TrashWindow.TrashingFinished.signal.connect(self.finished)
        self.ProgressStarted.signal.connect(self.started)
        self.ProgressReport.signal.connect(self.progress_report)
        self.ProgressFinished.signal.connect(self.finished)
        self.ProgressMessage.signal.connect(self.progress_message)
        self.show()
    
    def progress_message(self,msg):
        self.setWindowTitle(msg)
    def started(self,number):
        self.total=number
        self.progress_bar.setMaximum(number)
    def start_progress(self,thr):
        self.thr=thr
        self.thr.start()
        
    def progress_report(self,number):
        #percentage=(number*100.0)/self.total
        self.progress_bar.setValue(number)
        #self.setWindowTitle("%s "%percentage+"%")
    def keyPressEvent(self,event):pass    
    def finished(self,b):
        if b:
            try:self.thr.join()
            except:pass
            time.sleep(0.5)
            self.close()


#########################
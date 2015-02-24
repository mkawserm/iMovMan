'''
Created on Aug 3, 2013

@author: KaWsEr
'''




from PySide.QtCore import Qt
from PySide.QtGui import QWidget,QIcon
from modules.nimovman.core.config import appicon


class CoreWindow(QWidget):
    def __init__(self,*kwards,**kwargs):
        super(CoreWindow,self).__init__(None)
        self.type=None
        self.setWindowTitle("Core Window")
        self.setWindowIcon(QIcon(appicon("iMovMan")) )
        self.setFixedSize(450,350)

        
        self.hide()
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
    def setType(self,name):
        self.type=name
    def closeEvent(self,evnt):
        self.hide()
        evnt.ignore()

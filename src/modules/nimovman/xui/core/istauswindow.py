'''
Created on Aug 7, 2013

@author: KaWsEr
'''

from PySide.QtCore import Qt,QTimer#,QPropertyAnimation
from PySide.QtGui import QWidget,QLabel,QVBoxLayout,QDesktopWidget
#QGraphicsDropShadowEffect,QColor,#QPainter,QColor,QBrush

class iStatusWindow(QWidget):
    def __init__(self,parent=None):
        #self.mainwindow=parent
        super(iStatusWindow,self).__init__(None)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.TransparentMode|Qt.Tool)
        self.setStyleSheet(".QWidget{background:transparent;}")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        #self.setMaximumWidth(100)
        #self.setFocus(Qt.ActiveWindowFocusReason)
        
        #self.setFocusPolicy(Qt.NoFocus)
        #self.setEnabled(False)
        #self.setFocus(self.mainwindow)
        #self.clearFocus()
        self.setMinimumHeight(30)
        self.setMaximumHeight(30)
        self.setContentsMargins(0,0,0,0)
        self.status_text=QLabel(self)
        self.status_text.setContentsMargins(5,5,5,5)
        self.status_text.setText("")
        self.status_text.setStyleSheet("""
        QLabel{
        background-color: rgba(0, 0, 0, 75%);
        /*border:2px solid rgba(0, 0, 0, 75%);*/
        color:white;
        font:bold 8pt;
        border-radius:4px;
        
        }
        """)
        self.main_layout=QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(self.status_text)
        self.setLayout(self.main_layout)
        self.hide()
        
        self.status_time=1
        self.status_timer=QTimer()
        self.status_timer.timeout.connect(self.timeout)
        self.status_timer_counter=0
        #self.center()


        
    def timeout(self):
        self.clearFocus()
        self.status_timer_counter=self.status_timer_counter+1
        if self.status_timer_counter>=self.status_time:
            self.status_clear()
            self.status_timer.stop()
            self.status_timer_counter=0
            
            
    def status_clear(self):
        self.status_text.setText("")
        self.hide()
    def add_status(self,msg):
        self.status_timer.start(1000)
        self.status_text.setText(msg)
        pixelWidth = self.status_text.fontMetrics().width(self.status_text.text())


        self.resize(pixelWidth+10+100,self.height())
        self.center()
        self.show()
        #print self.windowState()==Qt.WindowState.WindowNoState
        #self.mainwindow.setFocus(Qt.Fo)
        #self.clearFocus()
    def position(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width()-5),screen.height()-size.height()-45)        
        
    def center(self):self.position()
    def enterEvent(self,evnt):pass
    def leaveEvent(self,evnt):pass
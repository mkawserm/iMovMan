'''
Created on Aug 19, 2013

@author: KaWsEr
'''

'''
Created on Aug 7, 2013

@author: KaWsEr
'''

from PySide.QtCore import Qt,QTimer#,QPropertyAnimation
from PySide.QtGui import QLabel,QVBoxLayout,QDesktopWidget
#QGraphicsDropShadowEffect,QColor,#QPainter,QColor,QBrush
from PySide import QtGui,QtCore
from modules.nimovman.core import util
from modules.nimovman.core import standardsignal
from modules.nimovman.core.dbmodel import Movie
from modules.nimovman.core import Log,error


RatingUpdated=standardsignal.SignalUnicode()


class RatingWindow(QtGui.QDialog):
    def __init__(self,vparent,path):
        #self.mainwindow=parent
        super(RatingWindow,self).__init__(None)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint|Qt.TransparentMode)
        self.setStyleSheet(""".QDialog{
        background:transparent;
        }""")
        self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setAttribute(Qt.WA_ShowWithoutActivating)
        #self.setAttribute(Qt.WA_NativeWindow)
        #self.setAttribute(Qt.WA_NoSystemBackground)
        self.setModal(True)
        #self.setMaximumWidth(100)
        #self.setFocus(Qt.ActiveWindowFocusReason)
        try:
            movieo=Movie()
            movie=movieo.get(path=path)[0]
        except:movie=None
        
        #self.setFocusPolicy(Qt.NoFocus)
        #self.setEnabled(False)
        #self.setFocus(self.mainwindow)
        #self.clearFocus()
        self.setFixedSize(400,200)
        #self.setMinimumHeight(300)
        #self.setMaximumHeight(300)
        self.setContentsMargins(0,0,0,0)
        #self
        self.path=path
        wid=QtGui.QWidget(self)
        wid.setFixedSize(400,100)
        wid.setContentsMargins(0,0,0,0)
        
        self.widget_layout=QtGui.QGridLayout()
        
        
        self.status_text=QLabel()
        self.status_text.setContentsMargins(5,5,5,5)
        self.status_text.setText("")
        self.status_text.setStyleSheet("""
        QLabel{
        background:transparent;
        color:white;
        font:15px bold;
        
        }
        """)

        self.widget_layout.addWidget(self.status_text,0,0,1,1)
        #self.widget_layout.setRowStretch(0,5)
        self.widget_layout.setColumnStretch(0,1)
        self.widget_layout.addItem(QtGui.QSpacerItem(500,200),1,0,2,2)

        self.save=QtGui.QPushButton("Save")
        self.save.setStyleSheet("""
        
            QPushButton {
                border:2px solid #8f8f91;
                border-radius: 5px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);
                min-width: 50px;
                max-width:50px;
                max-height:30px;
                }
            
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #dadbde, stop: 1 #f6f7fa);
                }
            
            QPushButton:flat {
                border: none; /* no border for a flat push button */
                }
            
            QPushButton:default {
                border-color: navy; /* make the default button prominent */
                }
                
        
        
        """)
        self.save.setFixedSize(50,25)
        #self.save.move(10,10)
        #self.save.setGeometry(10,10,10,10)
        #self.save.show()
        #self.widget_layout.addWidget(self.save,0,1,1,1)
        #self.widget_layout.addWidget(QtGui.QPushButton("Save2"),2,0,3,3)
        #self.widget_layout.setRowStretch(0,0)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 10)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.valueChanged)
        self.slider.setFocus(QtCore.Qt.FocusReason.ActiveWindowFocusReason)
        self.widget_layout.addWidget(self.slider,1,0,1,1)
        self.lcd = QtGui.QLCDNumber(2)
        self.lcd.setFrameStyle(QtGui.QFrame.NoFrame)
        
        
        # get the palette
        if movie!=None:
            self.lcd.display(int(movie.rating))
            self.slider.setValue(int(movie.rating))
            
        self.lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        palette = self.lcd.palette()
        # foreground color
        palette.setColor(palette.WindowText, QtGui.QColor(255, 0, 0))
        # background color
        palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))
        # "light" border
        palette.setColor(palette.Light, QtGui.QColor(255, 0, 0))
        # "dark" border
        palette.setColor(palette.Dark, QtGui.QColor(255, 0, 0))
        # set the palette
        self.lcd.setPalette(palette)
        self.widget_layout.addWidget(self.lcd,1,1,1,1)
        
        
        
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self.lcd, QtCore.SLOT("display(int)"))        

        wid.setLayout(self.widget_layout)
        
        self.main_layout=QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(wid)

        
        
        self.setLayout(self.main_layout)
        #self.hide()
        
        self.status_time=1
        self.status_timer=QTimer()
        #self.status_timer.timeout.connect(self.timeout)
        self.status_timer_counter=0
        self.center()
        
        
        
        self.add_status(util.get_name_from_path(self.path))

    
    
    def valueChanged(self,number):
        try:
            movieo=Movie()
            data={}
            data["path"]=self.path
            data["rating"]=number
            if movieo.update(data):
                Log("RatingWindow").info("%s Rating Updated..",self.path)
                RatingUpdated.signal.emit(self.path)
        except Exception,e:
            Log("RatingWindow").critical("%s %s",e,error())
        
    def paintEvent(self,event):
        painter=QtGui.QPainter(self)
        background=QtGui.QBrush(QtGui.QColor(0, 0, 0))
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setBrush(background)
        painter.setPen(Qt.NoPen)
        painter.setOpacity(0.9)
        painter.drawRoundedRect(0,0,self.width(),self.height(),7,7)


        
    def timeout(self):
        #self.clearFocus()
        self.status_timer_counter=self.status_timer_counter+1
        if self.status_timer_counter>=self.status_time:
            #self.status_clear()
            self.status_timer.stop()
            self.status_timer_counter=0
            self.close()
            
            
    def status_clear(self):
        self.status_text.setText("")
        self.hide()
    def add_status(self,msg):
        self.status_timer.start(1000)
        self.status_text.setText(msg)
        #pixelWidth = self.status_text.fontMetrics().width(self.status_text.text())


        #self.resize(pixelWidth+10+100,self.height())
        #self.center()
        #self.show()
        #print self.windowState()==Qt.WindowState.WindowNoState
        #self.mainwindow.setFocus(Qt.Fo)
        #self.clearFocus()
    def position(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        #self.move((screen.width()-size.width()-5),screen.height()-size.height()-45)        
        #self.move(QtGui.QCursor.pos())
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)
    def center(self):
        self.position()

    def wheelEvent(self,event):
        #print event
        pass
          
    def enterEvent(self,event):
        #print event
        self.slider.setFocus(QtCore.Qt.FocusReason.PopupFocusReason)
        self.status_timer.stop()
        self.status_timer_counter=0
    def leaveEvent(self,event):
        #pass
        #self.status_timer.start()
        self.close()
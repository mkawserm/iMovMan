'''
Created on Aug 20, 2013

@author: KaWsEr
'''
import weakref
from PySide import QtCore,QtGui
from modules.nimovman.core import config
from modules.nimovman.core.dbmodel import Movie
class PropertiesWindowA(QtGui.QDialog):
    def __init__(self,item):
        super(PropertiesWindowA,self).__init__(None)
        self.setWindowTitle(item.title)
        self.setWindowIcon(QtGui.QIcon(item.pix))
        self.setFixedSize(500,450)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.item=item

    
    def paintEvent(self,event):
        painter=QtGui.QPainter(self)
        background=QtGui.QBrush(QtGui.QColor(0, 0, 0))
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setBrush(background)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPixmap(0,0,self.item.pix)
        #painter.setOpacity(0.9)
        #painter.drawRect(0,0,self.width(),self.height())
        painter.drawRoundedRect(0,0,self.width(),self.height(),5,5)



class PropertiesWindow(QtGui.QDialog):
    def __init__(self,item):
        super(PropertiesWindow,self).__init__(None)
        self.setWindowTitle(item.title)
        self.setWindowIcon(QtGui.QIcon(item.pix))
        self.setFixedSize(500,500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.item=item
        self.tpos=0
        #self.form_text()
        self.setGeometry(300,300,500,500)

        #layout=QtGui.QGridLayout()
        self.setContentsMargins(0,0,0,0)
        
        self.doc=QtGui.QTextBrowser(self)
        self.doc.setFixedHeight(config.COVER_HEIGHT)
        self.doc.setFixedWidth(self.width()-config.COVER_WIDTH-5)
        self.doc.setStyleSheet("""
        .QTextBrowser{
        background:black;
        color:white;
        border:0px;
        font: 12pt "Impact";
        }
        """)
        

        
        
        data=""
        plot=""
        if self.item.movie_data.genre!="" and self.item.movie_data.genre!=None:
            data=data+"Genre: %s<br/><br/>"%self.item.movie_data.genre
        if self.item.movie_data.actors!="" and self.item.movie_data.actors!=None:
            data=data+"Actors: %s<br/>"%self.item.movie_data.actors
        if self.item.movie_data.director!="" and self.item.movie_data.director!=None:
            data=data+"Director: %s<br/>"%self.item.movie_data.director
        if self.item.movie_data.writer!="" and self.item.movie_data.writer!=None:
            data=data+"Writer: %s<br/>"%self.item.movie_data.writer
        if self.item.movie_data.released!="" and self.item.movie_data.released!=None:
            data=data+"Released: %s<br/>"%self.item.movie_data.released
        if self.item.movie_data.runtime!="" and self.item.movie_data.runtime!=None:
            data=data+"Runtime: %s<br/>"%self.item.movie_data.runtime
        if self.item.movie_data.rated!="" and self.item.movie_data.rated!=None:
            data=data+"Rated: %s<br/>"%self.item.movie_data.rated
        
        data="<br/>"+data
        if self.item.movie_data.rating!="" and self.item.movie_data.rating!=None and self.item.movie_data.rating!=0.0:
            data=data+"<br/>My Rating: %s<br/>"%self.item.movie_data.rating            
        if self.item.movie_data.tags!="" and self.item.movie_data.tags!=None:
            data=data+"Tag: %s<br/>"%self.item.movie_data.tags

        
              

        if self.item.movie_data.plot!="" and self.item.movie_data.plot!=None:
            plot=plot+"%s<br/>"%self.item.movie_data.plot 

        self.doc.setHtml(data)
        
        
        self.doc.move(config.COVER_WIDTH,0)
        #self.doc.setDocument(self.doc)
        #layout.setContentsMargins(0,0,0,0)
        #layout.addWidget(self.doc,10,0,0,0)
        #self.setLayout(layout)
        
        self.plot=QtGui.QTextBrowser(self)
        self.plot.setStyleSheet("""
        .QTextBrowser{
        background:black;
        color:white;
        border:0px;
        font: 13pt "Times New Roman";}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
        }
        """)
        self.plot.setHtml(plot)
        self.plot.setFixedSize(self.width()-5,self.height()-config.COVER_HEIGHT-5)
        self.plot.move(0,config.COVER_HEIGHT)
                
        
    def dragEnterEvent(self, event):
        event.ignore()
        
    def form_text(self):
        #pass
        movieo=Movie()
        data=movieo.map_single(self.item.movie_data)
        print data
        
    
#"""
    def paintEvent(self,event):
        painter=QtGui.QPainter(self)
        background=QtGui.QBrush(QtGui.QColor(0, 0, 0))
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setBrush(background)
        painter.drawRect(0,0,self.width(),self.height())#Back Drawn
        
                
        img=self.item.pix.scaled(config.COVER_WIDTH,config.COVER_HEIGHT, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        #painter.setBrush(img)
        painter.setPen(QtCore.Qt.NoPen)
        
        
        painter.drawPixmap(0,0,img)
        #background=
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        #painter.drawText(100,100,self.item.title,)
        #painter.setOpacity(0.9)

        info_rect = QtCore.QRectF(self.rect().left() +config.COVER_WIDTH, self.rect().top() + 4,
                                 self.rect().width() - 4, self.rect().height() - 4)
        



        font = painter.font()
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        #painter.setPen(QtCore.Qt.lightGray)
        #painter.drawText(textRect.translated(2, 2), message)
        #painter.setPen(QtCore.Qt.white)
        #painter.drawText(info_rect.translated(5,0),"Title: %s"%self.item.title)
        #painter.drawText(info_rect.translated(5,self.getTpos()),"Genre: %s"%self.item.movie_data.genre)
        #painter.drawText(info_rect.translated(5,self.getTpos()),"Actors: %s"%self.item.movie_data.actors)
        #painter.drawText(info_rect.translated(5,self.getTpos()),"Plot: %s"%self.item.movie_data.plot)
        
        
        #painter.drawRoundedRect(0,0,self.width(),self.height(),5,5)
        rating_rect=QtCore.QRectF(self.rect().left() +config.COVER_WIDTH-50, self.rect().top() + 4,self.rect().width() - 4, self.rect().height() - 4)
        effect = QtGui.QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(8)
        
        font.setPointSize(20)
        painter.setFont(font)
        #painter.s
        painter.setPen(QtCore.Qt.darkCyan)
        painter.drawText(rating_rect.translated(2, 2), unicode(self.item.movie_data.imdbrating) )
        painter.setPen(QtCore.Qt.yellow)
        painter.drawText(rating_rect, unicode(self.item.movie_data.imdbrating) )
    
    def getTpos(self):
        self.tpos=self.tpos+10+5
        return self.tpos
#"""
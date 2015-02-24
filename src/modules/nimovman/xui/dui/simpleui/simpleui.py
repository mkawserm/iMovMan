'''
Created on Aug 17, 2013

@author: KaWsEr
'''
'''
Created on Aug 12, 2013

@author: KaWsEr
'''



from PySide import QtGui,QtCore

from modules.nimovman.core import Log,error,standardsignal
from modules.nimovman.core import config

from modules.nimovman.core import imd
from modules.nimovman.xui.dui.mainwindow import MainWindow# This Will be overriden by SimpleUi



from widget_genre import GenreWidget
from widget_year import YearWidget
from widget_tag import TagWidget
from widget_moviegridlist import MovieGridList


### Global Variables ###
qc=QtCore
qg=QtGui

"""
Widget Design Technique
*Make Every widget Signal aware
"""
    





#############################################################
class SimpleUi(MainWindow):
    update_signal=standardsignal.MessageSendU()
    def __init__(self,*kwards,**kwargs):
        super(SimpleUi,self).__init__(*kwards,**kwargs)
        self.__name="SimpleUi"
        self.create_widgets()
        SimpleUi.update_signal.signal.connect(self.get_update_signal)
        
        
        self.init_signal_receivers()
        self.setObjectName("SimpleUi")
        self.setStyleSheet("""
        #SimpleUi{
        background-color: white;
        }
        
        """)
        self.setContentsMargins(0,0,0,0)


    def init_signal_receivers(self):
        """This Will interact with imd signal receivers"""
        imd.MovieAdder.MovieAdderStarted.signal.connect(self.sig_rec_movie_adder_started)
        imd.MovieAdder.MovieAdderFinished.signal.connect(self.sig_rec_movie_adder_finished)
        imd.MovieAdder.MovieAdderUpdates.signal.connect(self.sig_rec_movie_adder_updates)
        
    def sig_rec_movie_adder_started(self,msg):
        #print "MovieAdder:",msg
        pass
    def sig_rec_movie_adder_finished(self,msg):
        #print "MovieAdder:",msg
        pass
    def sig_rec_movie_adder_updates(self,msg):
        #print "MovieAdder:",msg
        pass


            
    def get_movie_signal(self,utype,msg):
        if utype=="updated":
            self.send_thumbnail_signal("refresh",msg)
        if utype=="deleted":
            self.send_thumbnail_signal("refresh",msg)
            

            
    def get_update_signal(self,utype,text):
        if utype=="status":
            #self.spin_start()
            self.statusBar().showMessage(text)
        elif utype=="spin":
            if text=="start":
                self.spin_start()
            elif text=="stop":
                self.spin_stop()
            

    def create_widgets(self):
        self.genre_widget=GenreWidget(self.widget_menu,self)
        self.genre_list=self.genre_widget.genre_list
        self.addDockWidget(qc.Qt.RightDockWidgetArea,self.genre_widget)
        #self.genre_list.SelectedClicked
        #self.genre_list.curre
        self.year_widget=YearWidget(self.widget_menu,self)
        self.year_list=self.year_widget.year_list
        self.addDockWidget(qc.Qt.RightDockWidgetArea,self.year_widget)
        
        self.tag_widget=TagWidget(self.widget_menu,self)
        self.tag_list=self.tag_widget.tag_list
        self.addDockWidget(qc.Qt.RightDockWidgetArea,self.tag_widget)        
        
        #self.year_widget.year_list.currentTextChanged.connect(self.year_changed)
        #self.genre_list.clicked.connect(self.genre_clicked)
        #self.genre_list.currentTextChanged.connect(self.genre_changed)
        #self.thw=ThumbnailWidget(self.widget_menu,self)
        #self.movie_list=self.thw.thumb.mlist
        #self.addDockWidget(qc.Qt.LeftDockWidgetArea,self.thw)
        #self.thw=Thumbnail(self)
        #self.movie_list=self.thw.mlist
        self.movie_grid_list=MovieGridList(self)
        self.movie_list=self.movie_grid_list.movie_list
        self.setContentsMargins(0,0,0,0)
        self.setCentralWidget(self.movie_grid_list)
        #self.movie_grid=MovieGrid(self)
        #self.setCentralWidget(self.movie_grid)
        #self.movie_grid_list.LoadStart.signal.emit()
        

    

        
    def genre_clicked(self,index):
        try:
            item=self.gw.genre_list.itemFromIndex(index)
            #print item.text()
        except:
            Log(self.__name).critical("Error while genre Clicked %s",error())
'''
Created on Aug 3, 2013

@author: KaWsEr
'''



import PySide
import threading
import webbrowser


## PySide ##
from PySide import QtCore
from PySide import QtGui
#from PySide import QtWebKit
## End PySide ##

from modules.nimovman.core import config
from modules.nimovman.core import kill
from modules.nimovman.core.imd import IMd
from modules.nimovman.core.config import appicon,asset



from modules.nimovman.xui.core.istauswindow import iStatusWindow
from modules.nimovman.xui.core import GuiRegister,GuiRegisterUpdate

#from moduels.nimovman.core.imd import IMd




from modules.nimovman.core import standardsignal
## Load Windows ##
from aboutwindow import AboutWindow
from moviesfolder import MoviesFolder
from settingswindow import SettingsWindow#,Test
from trashwindow import TrashWindow

#from simpleui import GenreWidget,Thumbnail,ThumbnailWidget





### Global Variables ###
ps=PySide
qc=QtCore
qg=QtGui
#qw=QtWebKit







#@util.onlyone
########## MainWindow ##########
class MainWindow(qg.QMainWindow):
    UpdateUi=standardsignal.MessageSendU()
    StatusSignal=standardsignal.SignalUnicode()
    GenreUpdated=standardsignal.Signal()
    YearUpdated=standardsignal.Signal()
    TagUpdated=standardsignal.Signal()
    MovieUpdated=standardsignal.Signal()
    def __init__(self,*kwards,**kwargs):
        super(MainWindow, self).__init__()
        
        self.main_window_signal=QtCore.Signal(int)
        
        
        self.setMinimumHeight(600)
        self.setMinimumWidth(900)
        self.initialize()
        self.non_gui_initilize()

        
        
        #Create Widgets
        #self.main_window_signal.connect(self.main_window_signal_loaded)
        #self.main_window_signal.emit(1)

        #self.create_widgets()
        
        ## Initialize Others
        self.statusbar_init()
        
        self.StatusSignal.signal.connect(self.add_msg)
        self.old_state=self.windowState()
        self.setObjectName("MainWindow")         


    def add_msg(self,msg):
        self.istatus.add_status(msg)
        

        
    def initialize(self):
        self.areas=QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        self.exareas=self.areas | QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.TopDockWidgetArea
        
        self.gui_register=GuiRegister.Instance()
        self.gui_register_update=GuiRegisterUpdate()
        self.gui_register_update.signal.connect(self.gui_update_receiver)
        self.gui_register.add_update_receiver(self.gui_register_update,"full")
        self.main_layout=qg.QVBoxLayout()
        
        
        ## Load Windows ##
        self.loaded_windows={}
        
        
        # Help Menu Section #
        # Help Window Section #
        self.help_action=qg.QAction(qg.QIcon(appicon("act_help")),"Help",self )
        self.help_action.setShortcut("F1")
        self.help_action.triggered.connect(self.action_help_window)
        try:self.gui_register.add_help_action(self.help_action)
        except:pass
        # End Help Window Section #
        
        # About Window Section #
        self.loaded_windows["about"]=AboutWindow()
        self.about_action=qg.QAction(qg.QIcon(appicon("act_about")),"About",self )
        self.about_action.setShortcut("F2")
        self.about_action.triggered.connect(self.action_about_window)
        try:self.gui_register.add_help_action(self.about_action)
        except:pass
        # End About Window Section #
        
        # Like me Window Section #
        self.like_me_action=qg.QAction(qg.QIcon(appicon("act_facebook")),"Like Me",self )
        self.like_me_action.setShortcut("F3")
        self.like_me_action.triggered.connect(self.action_like_me)
        try:self.gui_register.add_help_action(self.like_me_action)
        except:pass
        # End Help Menu Section #
        
        
        
        # Options Menu #
        self.loaded_windows["settings"]=SettingsWindow(self)
        
        self.settings_action=qg.QAction(qg.QIcon(appicon("act_settings")),"Settings",self )
        #self.settings_action.setShortcut("S")
        self.settings_action.triggered.connect(self.action_settings)
        try:self.gui_register.add_options_action(self.settings_action)
        except:pass
        ## End Options Menu ##
        
        
        
        
        ## File Menu ##
        self.movie_menu=qg.QMenu("Movie")
        self.movie_menu.setIcon( qg.QIcon(appicon("menu_movie")) )
        #self.movie_menu.setStatusTip("Manage Movies")
        
        #Load Movies Folder
        self.loaded_windows["movies_folder"]=MoviesFolder()
        
        #Add Movies#
        self.movie_add_action=qg.QAction(qg.QIcon(appicon("act_add")),"Add",self)
        self.movie_add_action.setShortcut("Shift+A")
        self.movie_add_action.setStatusTip("Add Movie's Folder")
        self.movie_add_action.triggered.connect(self.action_movie_add)
        self.movie_menu.addAction(self.movie_add_action)
        
        #Scan Movies#
        self.movie_scan_action=qg.QAction(qg.QIcon(appicon("act_scan")),"Scan",self)
        self.movie_scan_action.setShortcut("Shift+S")
        self.movie_scan_action.setStatusTip("Scan Movies and add new movies and delete non existing movies from database")
        self.movie_scan_action.triggered.connect(self.action_movie_scan)
        self.movie_menu.addAction(self.movie_scan_action)
        
        
        
        #Movies
        #self.movies_action=qg.QAction(qg.QIcon(appicon("act_movies")),"Movies",self)
        #self.movies_action.setStatusTip("Browse All Movies")
        #self.movies_action.setShortcut("Shift+M")
        #self.movie_menu.addAction(self.movies_action)
        
        #Movies Trash
        self.loaded_windows["trash"]=TrashWindow(self)
        self.movies_trash_action=qg.QAction(qg.QIcon(appicon("act_trash")),"Trash",self)
        self.movies_trash_action.setStatusTip("Browse All Trashed Movies")
        self.movies_trash_action.setShortcut("Shift+T")
        self.movies_trash_action.triggered.connect(self.action_trash)
        self.movie_menu.addAction(self.movies_trash_action)        
        

        try:self.gui_register.add_file_menu(self.movie_menu)
        except:pass
        
        self.exit_action = qg.QAction(qg.QIcon(appicon("act_exit")),"Exit",self)
        self.exit_action.setShortcut("Shift+Q")
        self.exit_action.setStatusTip("Exit iMovMan")
        self.exit_action.triggered.connect(self.action_exit)
        try:self.gui_register.add_file_action(self.exit_action)
        except:pass   
        ## End File Menu ##
        
        #print self.gui_register.get_file_menu()
        
        
        #print dir(self.gui_register.get_file_menu())
        
        self.icon=appicon("iMovMan")
        self.title="iMovMan"
        
        self.setWindowIcon(qg.QIcon(self.icon))
        self.setWindowTitle(self.title)
        self.setMinimumHeight(self.height()-self.height()*0.3)
        self.setMinimumWidth(self.width()-self.width()*0.2)
        
        self.statusBar().setMinimumHeight(20)
        self.setMenuBar(self.gui_register.get_menu_bar())
        #self.showMaximized()
        
        

        #self.main_layout.addItem(qg.QSpacerItem(self.width(),self.height()))
        #self.main_layout.addWidget(self.istatus)
        #self.setCentralWidget(self.istatus)
        #self.istatus.add_status("What are you doing")
        #self.main_layout.addWidget(qg.QLabel("Smile as",self))
        #self.main_layout.addItem(qg.QSpacerItem(2000,2000))
        #self.main_layout.addWidget(self.istatus)
        #self.setLayout(self.main_layout)
        #self.simpleui=SimpleUi(self)
        #self.cwidget=CentralWidget(self)
        #self.setCentralWidget(self.simpleui)
        
        
        ###iStatusWindow###
        self.istatus=iStatusWindow()
        
        self.ct_menu=qg.QMenu("Menu")
        self.widget_menu=qg.QMenu("Widgets")
        self.widget_menu.setIcon(qg.QIcon(appicon("widget")))
        self.ct_menu.addMenu(self.widget_menu)
        
        
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)
        

    def statusbar_init(self):
        #self.statusBar().setMaximumheight(25)
        self.spinner_screen=QtGui.QLabel(self.statusBar())
        self.spinner = qg.QMovie(config.appanim("anim"), qc.QByteArray(), self)
        self.spinner.setCacheMode(qg.QMovie.CacheAll)
        self.spinner.setSpeed(200)
        
        self.spinner_screen.setMinimumWidth(25)
        self.spinner_screen.setMaximumWidth(25)
        
        self.spinner_screen.setMinimumHeight(25)
        self.spinner_screen.setMaximumHeight(25)
        self.spinner_screen.setMovie(self.spinner)
        self.spinner_screen.hide()
        self.statusBar().addPermanentWidget(self.spinner_screen)

    def spin_start(self):
        self.spinner_screen.show()
        self.spinner.start()
        
    def spin_stop(self):
        self.spinner.stop()
        self.spinner_screen.hide()
    
    def contextMenuEvent(self, event):
        self.ct_menu.exec_(QtGui.QCursor.pos())  
    
    

    def non_gui_initilize(self):
        self.imd=IMd(self)
        #print "Track"
        #print IMd.Instance()
        
    
    """Define All Actions methods here"""
    def action_like_me(self):webbrowser.open_new(config.APP_FB)
    def action_help_window(self):webbrowser.open_new(config.APP_HELP)
    def action_settings(self):self.loaded_windows["settings"].show()
    def action_about_window(self):self.loaded_windows["about"].show()
    def action_movie_add(self):self.loaded_windows["movies_folder"].show()
    def action_trash(self):self.loaded_windows["trash"].show()
    
    def action_movie_scan(self):
        #print "Scanning Movies"
        self.istatus.add_status("Scanning Movies....")

        if not self.imd.movie_adder.is_auto_scan_enabled():
            try:
                if not self.athr.isAlive():
                    self.athr.start()
                #else:print "Alive"
            except:
                self.athr=threading.Thread(target=self.imd.movie_adder.scan)
                self.athr.setDaemon(True)
                self.athr.start()
            #self.imd.movie_adder.scan()
        if not self.imd.movie_remover.is_auto_delete_enabled():
            try:
                if not self.dthr.isAlive():
                    self.dthr.start()
            except:
                self.dthr=threading.Thread(target=self.imd.movie_remover.delete)
                self.dthr.setDaemon(True)
                self.dthr.start()
        
    def action_exit(self):
        self.close()
        app=qg.QApplication.instance()
        if app!=None:
            app.exit()
            kill.do()
    """End All Actions method"""
    
    
    
    
        
    def gui_update_receiver(self,msg):
        """Update Receiver from GuiRegister"""
        self.setMenuBar(self.gui_register.get_menu_bar())
        
    
    
    #Events#

    def closeEvent(self,evnt):
        self.hide()
        evnt.accept()
        app=qg.QApplication.instance()
        if app!=None:
            app.exit()
            kill.do()
        
    def resizeEvent(self,event):
        pass
        #self.old_state=self.windowState()
        #print evnt
        #self.istatus.center()
        #print "call"
        #print self.width(),self.height()
    def keyReleaseEvent(self,event):
        pass
        #print event
    
    def mouseReleaseEvent(self,event):
        #print event.button
        if event.button==qc.Qt.LeftButton:
            print "Right"
            
    def keyPressEvent(self,evnt):
        #print self.windowState()==qc.Qt.WindowFullScreen
        if evnt.key()==qc.Qt.Key_F1:
            self.action_help_window()
        #if evnt.key()==qc.Qt.Key_M:
        #    self.widget_menu.addAction("Menu")
        #    self.widget_menu.exec_(QtGui.QCursor.pos())
                
        elif evnt.key()==qc.Qt.Key_F11 or evnt.key()==qc.Qt.Key_F:#FullScreenLogic
            if self.windowState()!=qc.Qt.WindowFullScreen:
                self.old_state=self.windowState()
                self.showFullScreen()
            elif self.windowState()==qc.Qt.WindowFullScreen:
                self.showMaximized()
                #self.setWindowState(self.old_state)
    
    def Instance(self):return self
    
        


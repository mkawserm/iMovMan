'''
Created on Aug 13, 2013

@author: KaWsEr
'''
from PySide.QtGui import QMenu,QAction,QIcon
#from PySide.QtCore import SIGNAL,SLOT
from PySide import QtGui

from modules.nimovman.core import Log,error
from modules.nimovman.core.config import appicon
#from modules.nimovman.core.dbmodel import Option,Trash,Movie
from modules.nimovman.core.dbmodel import Option

#from modules.nimovman.core.immjob import *
from modules.nimovman.core import util
from modules.nimovman.core.immjob import get_drives_details
from modules.nimovman.core import standardsignal
from modules.nimovman.core import config







class SendtoAction(QAction):
    def __init__(self,name,drive,parent):
        super(SendtoAction,self).__init__(name,parent)
        self.setIcon(QIcon(appicon("drive")))
        self.drive=drive
        
class SortbyAction(QAction):
    def __init__(self,name,parent):
        super(SortbyAction,self).__init__(name,parent)
        self.setIcon(QIcon(appicon("sort")))



class MovieMenu(QMenu):
    SelectedDrive=standardsignal.MessageSendU()
    Sortby=standardsignal.SignalUnicode()
    def __init__(self,parent,menutype="single"):
        self.__name="MovieMenu"
        super(MovieMenu,self).__init__(parent)
        self.menutypes=["single","multiple","none"]
        self.menutype=menutype.lower()
        self.show_favourite=True
        #self.show_unfavourite=True
        self.show_watched=True#0 un #1 watched #2want to watch
        self.show_wishlist=True
    
    
    def make(self):
        self.drives=get_drives_details()
        #self.send_to=self.drive_menu()
        self.selected_drive=None
        self.__menus=[]
        
        if self.show_watched:
            self.watched=QAction(QIcon(appicon("watched")),"Watched",self )
        else:
            self.watched=QAction(QIcon(appicon("unwatched")),"UnWatched",self)
        self.__menus.append(self.watched)

        #elif self.show_watched==2:
            #self.watched=QAction(QIcon(appicon("wanttowatch")),"Wish List",self )
        if self.show_favourite:
            self.favourite=QAction(QIcon(appicon("favourite")),"Favourite",self )
        else:
            self.favourite=QAction(QIcon(appicon("unfavourite")),"UnFavourite",self )
        self.__menus.append(self.favourite)
               
        if self.show_wishlist:
            self.wish_list=QAction(QIcon(appicon("wanttowatch")),"Wish List",self )
        else:
            self.wish_list=QAction(QIcon(appicon("wanttowatch")),"Remove From Wish List",self )
        
        
        self.__menus.append(self.wish_list)
        
        self.play=QAction(QIcon(appicon("play")),"Play",self )
        self.__menus.append(self.play)
        
        self.explore=QAction(QIcon(appicon("explore")),"Explore",self )
        self.__menus.append(self.explore)
        
        self.refresh=QtGui.QAction(QIcon(appicon("refresh")),"Refresh",self)
        self.__menus.append(self.refresh)
        
        self.edit=QAction(QIcon(appicon("edit")),"Edit",self )
        self.__menus.append(self.edit)
        
        self.add_tag=QAction(QIcon(appicon("add")),"Add Tag",self )
        self.__menus.append(self.add_tag)
        
        
        self.change_cover=QAction(QIcon(appicon("replace")),"Change cover",self )
        self.__menus.append(self.change_cover)
        
        self.update_imdb_id=QAction(QIcon(appicon("update")),"Update IMDb id",self )
        self.__menus.append(self.update_imdb_id)
        
        self.open_imdb=QAction(QIcon(appicon("imdb")),"Open IMDb",self )
        self.__menus.append(self.open_imdb)
        
        self.properties=QAction(QIcon(appicon("properties")),"Properties",self )
        self.__menus.append(self.properties)
        
        self.delete=QAction(QIcon(appicon("delete")),"Delete",self )
        self.__menus.append(self.delete)
        
        self.rate_it=QAction(QIcon(appicon("rate")),"Rate It",self )
        self.__menus.append(self.rate_it)
        
        
        if self.menutype=="single":
            self.addAction(self.play)
            self.addAction(self.explore)
            self.addAction(self.open_imdb)
            self.addSeparator()
            self.addAction(self.add_tag)
            self.addSeparator()
            self.addAction(self.edit)
            self.addAction(self.rate_it)
            self.addAction(self.change_cover)
            self.addAction(self.update_imdb_id)

            self.addSeparator()
        if self.menutype=="single" or self.menutype=="multiple" or self.menutype=="none":
            self.addMenu(self.sort_menu())           
        self.addAction(self.refresh)
        self.addSeparator()
        
        
        if self.menutype=="single" or self.menutype=="multiple":
            self.addAction(self.favourite)
            self.addSeparator()
            self.addAction(self.wish_list)
            self.addSeparator()
            
            
            self.addAction(self.watched)
            self.addSeparator()    
            self.addAction(self.delete)
            self.addSeparator()
        if self.menutype=="single":
            self.addAction(self.properties)
        if self.menutype=="single" or self.menutype=="multiple":
            self.addMenu(self.drive_menu())
        #self.connect(self, SIGNAL("triggered(QAction)"), self, SLOT("self.click_drive_menu(QAction*)"))
        #self.triggered.connect(self.click_drive_menu)
        
    def register(self,act,func):
        act.triggered.connect(func)

    def register_all(self,func):
        for menu in self.__menus:
            menu.triggered.connect(func)
                
    def click_event(self):
        if type(self.sender())==SendtoAction:
            self.selected_drive=self.sender().drive
            try:
                option=Option()
                opt=option.get_option("send_to")
                index=config.SEND_TO.index(opt)
                if index==2:
                    self.send_to_popup()
                else:
                    #print self.selected_drive,opt
                    self.SelectedDrive.signal.emit(self.selected_drive,opt)
            except:pass
        if type(self.sender())==QAction:
            self.SelectedDrive.signal.emit(self.selected_drive,self.sender().text())
        if type(self.sender())==SortbyAction:
            self.Sortby.signal.emit(unicode(self.sender().text().lower()))
            
            
        """
        if type(self.sender())==QAction:
            act=self.sender().text().lower()
            
            if act=="play":#checked
                Log(self.__name).info("Play initiating : %s",self.path)
                try:file_play(self.path)
                except Exception,e:Log(self.__name).critical("%s %s",e,error())
                
            elif act=="explore":#checked
                Log(self.__name).info("Explore initiating : %s",self.path)
                try:
                    explore(os.path.dirname(self.path))
                except Exception,e:
                    Log(self.__name).critical("%s %s",e,error())
                    
            elif act=="delete":#checked
                reply = QtGui.QMessageBox.question(self.vparent,
                                                   "Delete %s?"%self.item.title,
                                                   "Are you sure to delete  %s from database?"%self.item.title,
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                
                if reply == QtGui.QMessageBox.Yes:
                    Log(self.__name).info("Delete initiating : %s",self.path)
                    try:
                        trash=Trash()
                        tadd=trash.add(self.path)
                        Log(self.__name).info("Trash Add : %s",tadd)
                        movie=Movie()
                        mdel=movie.delete(self.path)
                        Log(self.__name).info("Movie Delete : %s",mdel)
                        trashwindow.TrashWindow.TrashDataReset.signal.emit(1)
                    except Exception,e:
                        Log(self.__name).critical("%s %s",e,error())
                else:
                    Log(self.__name).info("Delete Cancelled : %s",self.path)
                    
                
        """        




    def sort_menu(self):
        sort_by=QMenu("Sort By")
        sort_by.setIcon( QIcon(appicon("default_menu")) )
        sorting=["Year","Title","Oldest","Newest","My Rating","IMDb Rating","ASC","DESC"]
        for i in sorting:
            k=SortbyAction(i,self)
            k.triggered.connect(self.click_event)
            sort_by.addAction(k)
        return sort_by
        
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
        return send_to
    
    
    def send_to_popup(self):
        drive_option=QMenu(self.parent())
        opts=config.SEND_TO[0:(len(config.SEND_TO)-1)]
        for cnf in opts:
            k=QAction(QIcon(appicon("explore")),cnf,self )
            k.triggered.connect(self.click_event)
            drive_option.addAction(k)
        drive_option.exec_(QtGui.QCursor.pos())
        
        
        
        
        
        
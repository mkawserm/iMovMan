'''
Created on Aug 17, 2013

@author: KaWsEr
'''


from PySide import QtGui,QtCore
#from modules.nimovman.core import imd
from modules.nimovman.core.dbmodel import Movie
from modules.nimovman.core import Log,error,config
from tageditorwindow import TagUpdated

class TagWidget(QtGui.QDockWidget):
    def __init__(self,menu,parent):
        super(TagWidget,self).__init__("Tags",parent)
        self.setMaximumWidth(250)
        self.setAllowedAreas(parent.areas)
        
        self.tag_list = QtGui.QListWidget(self)
        self.setWidget(self.tag_list)
        self.data_reset()
        menu.addAction(self.toggleViewAction())
        TagUpdated.signal.connect(self.data_reset)
        
        reset=QtGui.QAction(QtGui.QIcon(config.appicon("refresh")),"Reset",self)
        reset.triggered.connect(self.data_reset)
        self.addAction(reset)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
            
    def data_reset(self):
        movie = Movie()
        self.tag_list.clear()
        try:
            data=Movie().get_tags()
            data=data.split(",")
        except:pass
        unwatched = len( movie.get() ) - len(movie.get_by_tag("watched"))
        pre_item=["All",
                  "Wish List"+" (" +  str ( len( movie.get_by_tag("Wish List") ) ) +")",
                  "Watched"+" (" +  str ( len( movie.get_by_tag("Watched") ) ) +")",
                  "Unwatched"+" (" +  str (  unwatched ) +")",
                  "Favourite"+" (" +  str ( len( movie.get_by_tag("Favourite") ) ) +")"]
        for item in pre_item:
            self.tag_list.addItem(item)
        #self.tag_list.addItem(u"All")
        self.tag_list.setCurrentIndex(self.tag_list.rootIndex())
        if data!=None:
            #data.append("All")
            data.sort()
            #data.reverse()
            for i in data:
                try:
                    if i.lower()!="all" and i.lower()!="watched" and i.lower()!="favourite" and i.lower()!="wish list" and i !="":
                        if str(i).capitalize()==unicode(i):
                            self.tag_list.addItem(i)
                        else:
                            self.tag_list.addItem(str(i).capitalize()  +" (" +  str ( len( movie.get_by_tag(i) ) ) +")" )
                except:
                    Log("TagWidget").critical("Add Item Failed: %s",error())    
################################################################################
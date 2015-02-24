'''
Created on Aug 17, 2013

@author: KaWsEr
'''
from PySide import QtGui
from modules.nimovman.core import imd
from modules.nimovman.core.dbmodel import Option,Movie
from modules.nimovman.core import Log,error




###################################Widget Collection######################
class GenreWidget(QtGui.QDockWidget):
    def __init__(self,menu,parent):
        super(GenreWidget,self).__init__("Genre",parent)
        self.setMaximumWidth(250)
        self.setAllowedAreas(parent.areas)
        self.genre_list = QtGui.QListWidget(self)
        self.setWidget(self.genre_list)
        self.data_reset()
        #self.parent.addDockWidget(self.areas,genre)
        menu.addAction(self.toggleViewAction())
        #self.genre_list.currentTextChanged.connect(self.genre_select)
        imd.MovieUpdater.MovieUpdaterGenreUpdated.signal.connect(self.data_reset)
        
    
    def data_reset(self):
        movie = Movie()
        self.genre_list.clear()
        self.genre_list.addItem(u"All" +" (" +  str ( len( movie.get() ) ) +")" )
        try:data=Option().get_option("option_genre")
        except:pass
        if data!=None:
            #data.append("All")
            data.sort()
            for i in data:
                
                try:
                    
                    self.genre_list.addItem(i.capitalize() +" (" +  str ( len( movie.get_by_genre(i) ) ) +")")
                except:
                    Log("GenreWidget").critical("Add Item Failed: %s",error())
        return True
                    
########
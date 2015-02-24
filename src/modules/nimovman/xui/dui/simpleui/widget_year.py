'''
Created on Aug 17, 2013

@author: KaWsEr
'''
from PySide import QtGui
from modules.nimovman.core import imd
from modules.nimovman.core.dbmodel import Option
from modules.nimovman.core import Log,error
from modules.nimovman.core.dbmodel import Movie


class YearWidget(QtGui.QDockWidget):
    def __init__(self,menu,parent):
        super(YearWidget,self).__init__("Year",parent)
        self.setMaximumWidth(250)
        

        
        self.setAllowedAreas(parent.areas)
        self.year_list = QtGui.QListWidget(self)
        self.setWidget(self.year_list)
        self.data_reset()
        
        
        #self.parent.addDockWidget(self.areas,genre)
        menu.addAction(self.toggleViewAction())
        #self.genre_list.currentTextChanged.connect(self.genre_select)
        imd.MovieUpdater.MovieUpdaterYearUpdated.signal.connect(self.data_reset)
    def data_reset(self):
        movie = Movie()
        self.year_list.clear()
        try:data=Option().get_option("option_year")
        except:pass
        self.year_list.addItem(u"All")
        if data!=None:
            #data.append("All")
            data.sort()
            data.reverse()
            for i in data:
                try:
                    self.year_list.addItem(str(i)  +" (" +  str ( len( movie.get_by_year (i) ) ) +")"   )
                except:
                    Log("YearWidget").critical("Add Item Failed: %s",error())
###############
'''
Created on Aug 3, 2013

@author: KaWsEr
'''



import os
import sys
import PySide
from PySide import QtGui
from modules.nimovman.core import config
from modules.nimovman.core.dbmodel import Option


from modules.nimovman.xui.core import PluginLoader
#from modules.nimovman.xui.core import GuiRegister,GuiRegisterUpdate






## Load MainWindow ##
from modules.nimovman.core import util
from modules.nimovman.core import Log,error










QApplication=QtGui.QApplication


class UiLoader(object):
    def __init__(self):
        self.load_mapis()#Load Movie Fetcher APIS
        self.qapp = QApplication(sys.argv)
        
        qApp = QApplication.instance()
        for plugins_dir in [os.path.join(p, "plugins") for p in PySide.__path__]:
            qApp.addLibraryPath(plugins_dir)        

        
        
        self.setup()
        #print QApplication.applicationDirPath()
        plugins=os.path.join(util.get_app_path(),"plugins")
        Log("UiLoader").debug("PLUGIN PATH : %s",plugins)
        QApplication.addLibraryPath(plugins)
        #print QApplication.libraryPaths()   
        Log("UiLoader").debug("PATH: %s",QApplication.libraryPaths())
        #self.initilize()

        
        
        
        
        
        
        
        
        
        self.simpleui_initilize()
        self.plugin_loader()
        Log("UiLoader").debug("UiLoader initialized")
        self.qapp.exec_()
    
    def simpleui_initilize(self):
        from simpleui.simpleui import SimpleUi
        self.simple_ui=SimpleUi(self)
        self.simple_ui.show()
        self.simple_ui.statusBar().showMessage("SimpleUi ready",5000)
        
    def mainwindow_initilize(self):
        from mainwindow import MainWindow
        self.mainwindow=MainWindow(self)
        self.mainwindow.show()
        #self.mainwindow.showMaximized()
        self.mainwindow.statusBar().showMessage("iMovMan ready",5000)
    
    
    def load_mapis(self):
        for i in util.get_movie_fetcher_apis_zipped(config.C_MAPI_PATH):
            if i.endswith("zip"):
                #print i
                sys.path.insert(0, os.path.join(config.C_MAPI_PATH,i))
                
        
        

        
    def plugin_loader(self):
        self.plugin_loader=PluginLoader.Instance()
        self.plugin_loader.load_plugins()
            
    def setup(self):
        """Setup The System"""
        try:
            self.option=Option()
            if not self.option.has_option("setup"):
                self.default()
                Log("UiLoader").debug("Database Setup Complete")
            self.option.vaccum()
        except Exception,e:
            Log("UiLoader").critical(error(),e)
            
    def default(self):
        self.option.replace("C_MOVIE_FORMAT",config.C_MOVIE_FORMAT)
        self.option.replace("C_COVER_FORMAT",config.C_COVER_FORMAT)
        self.option.replace("cover_dir",config.DATA_DIR[0])
        self.option.replace("data_dir",config.DATA_DIR[0])
        self.option.replace("auto_scan",config.EN_DIS[1])
        self.option.replace("auto_delete",config.EN_DIS[1])
        self.option.replace("title_style","%title% (%year%)")
        self.option.replace("movie_api", config.C_DEFAULT_API)
        self.option.replace("send_to",config.SEND_TO[0])
        self.option.replace("setup","setup-full")
        
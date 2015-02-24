'''
Created on Aug 2, 2013

@author: KaWsEr
'''
from PySide.QtCore import Signal,QObject
from PySide.QtGui import QMenuBar,QMenu,QAction
from modules.nimovman.core.util import onlyone
from pluginloader import PluginLoader

class GuiRegisterUpdate(QObject):
    signal=Signal(str)


@onlyone
class GuiRegister(object):
    def Instance(self):return self
    
    def __init__(self,*kwards,**kwargs):
        #self.grs=GuiRegisterUpdate()#Gui Register Signal
        """If anything updated by plugin or any other gui part this
        list hold the update receivers.If any thing change update receiver list
        will be notified.And this list must be GuiRegisterUpdate object
        """
        self.__update_receiver_list=[]#This will get update notice
        self.__menu_bar=QMenuBar()
        self.__file_menu=self.__menu_bar.addMenu("&File")
        self.__options_menu=self.__menu_bar.addMenu("&Options")
        
        #self.__plugins_menu=self.__menu_bar.addMenu("&Plugins")
        self.__plugins_menu=QMenu()
        self.__registered_plugins_menu={}
        
        #self.__tools_menu=self.__menu_bar.addMenu("&Tools")
        self.__tools_menu=QMenu()
        self.__registered_tools_menu={}
        
        self.__help_menu=self.__menu_bar.addMenu("&Help")
        self.__movie_menu=QMenu()
        
        self.__menus=["&File",
                      "&Options",
                      #"&Plugins",
                      #"&Tools",
                      "&Help"]
        
        
        self.__plugin_loader=PluginLoader.Instance()
        
    
    def get_menu_bar(self):return self.__menu_bar
    def __send_update(self,*kwards,**kwargs):
        gru_type=None
        if len(kwards)==1:
            gru_type=kwards[0]
            
        for url in self.__update_receiver_list:
            if url[1] == gru_type:
                url[0].signal.emit("True")
            elif url[1] == "full":
                url[0].signal.emit("True")
    
    def update(self):self.__send_update()
    
    
    
    def add_file_action(self,*kwards,**kwargs):
        if len(kwards)==1:
            help_action=kwards[0]
            if type(help_action) == QAction:
                self.__file_menu.addAction(help_action)
                self.__send_update("help-menu")
                return True
            else:raise TypeError("Argument Type Must be a QAction object")
        return False

    def add_file_menu(self,*kwards,**kwargs):return self.register_file_menu(*kwards,**kwargs)
    def register_file_menu(self,*kwards,**kwargs):
        if len(kwards)==1:
            file_menu=kwards[0]
            if type(file_menu) == QMenu:
                self.__file_menu.addMenu(file_menu)
                self.__send_update("file-menu")
                return True
            else:raise TypeError("Argument Type Must be a QMenu object")
        return False
    def get_file_menu(self):return self.__file_menu


    def add_options_menu(self,*kwards,**kwargs):return self.register_options_menu(*kwards,**kwargs)
    def register_options_menu(self,*kwards,**kwargs):
        if len(kwards)==1:
            option_menu=kwards[0]
            if type(option_menu) == QMenu:
                self.__options_menu.addMenu(option_menu)
                self.__send_update("options-menu")
                return True
            else:raise TypeError("Argument Type Must be a QMenu object")
        return False
    
    def add_options_action(self,*kwards,**kwargs):
        if len(kwards)==1:
            help_action=kwards[0]
            if type(help_action) == QAction:
                self.__options_menu.addAction(help_action)
                self.__send_update("options-menu")
                return True
            else:raise TypeError("Argument Type Must be a QAction object")
        return False
    
    
    def add_plugins_menu(self,*kwards,**kwargs):return self.register_plugins_menu(*kwards,**kwargs)
    
    def register_plugins_menu(self,*kwards,**kwargs):
        if len(kwards)==2:
            plugin_name=kwards[0]
            plugin_menu=kwards[1]
            if type(plugin_menu) == QMenu:
                self.__registered_plugins_menu[plugin_name]=plugin_menu
                self.update_plugins_menu()
                self.__send_update("plugins-menu")
                return True
            else:raise TypeError("Argument Type Must be a QMenu object")
        return False
   
    def update_plugins_menu(self):
        self.__plugins_menu.clear()
        for plugin_name in self.__registered_plugins_menu.keys():
            self.__plugins_menu.addMenu( self.__registered_plugins_menu[plugin_name])
    def update_tools_menu(self):
        self.__tools_menu.clear()
        for tool_name in self.__registered_tools_menu.keys():
            self.__tools_menu.addMenu( self.__registered_tools_menu[tool_name])
    
    def delete_plugins_menu(self,*kwards,**kwargs):return self.deregister_plugins_menu(*kwards,**kwargs)
           
    def deregister_plugins_menu(self,*kwards,**kwargs):
        if len(kwards)==1:
            plugin_name=kwards[0]
            del self.__registered_plugins_menu[plugin_name]
            self.update_plugins_menu()
            self.__send_update("plugins-menu")
            return True
        return False


    def add_tools_menu(self,*kwards,**kwargs):return self.register_tools_menu(*kwards,**kwargs)
    def register_tools_menu(self,*kwards,**kwargs):
        if len(kwards)==2:
            plugin_name=kwards[0]
            plugin_menu=kwards[1]
            if type(plugin_menu) == QMenu:
                self.__registered_tools_menu[plugin_name]=plugin_menu
                self.update_tools_menu()
                self.__send_update("tools-menu")
                return True
            else:raise TypeError("Argument Type Must be a QMenu object")
        return False


    def add_help_menu(self,*kwards,**kwargs):return self.register_help_menu(*kwards,**kwargs)
    def register_help_menu(self,*kwards,**kwargs):
        if len(kwards)==1:
            help_menu=kwards[0]
            if type(help_menu) == QMenu:
                self.__help_menu.addMenu(help_menu)
                self.__send_update("help-menu")
                return True
            else:raise TypeError("Argument Type Must be a QMenu object")
        return False
    
    def add_help_action(self,*kwards,**kwargs):
        if len(kwards)==1:
            help_action=kwards[0]
            if type(help_action) == QAction:
                self.__help_menu.addAction(help_action)
                self.__send_update("help-menu")
                return True
            else:raise TypeError("Argument Type Must be a QAction object")
        return False


 
    def register_update_receiver(self,*kwards,**kwargs):
        gru=None
        if len(kwards)==2:
            gru=kwards[0]
            gru_type=kwards[1]
        
        if type(gru)==GuiRegisterUpdate and type(gru_type)==str:
            self.__update_receiver_list.append([gru,gru_type])
            return True
        else:raise TypeError("Argument Type Must be a GuiRegisterUpdate object")
        return False
    def add_update_receiver(self,*kwards,**kwargs):return self.register_update_receiver(*kwards,**kwargs)
    
    
    def get_plugin(self,name):return self.__plugin_loader.get_plugin(name)        
    
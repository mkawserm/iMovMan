'''
Created on Aug 2, 2013

@author: KaWsEr
'''
import os
#import types

from modules.nimovman.core import Log,error
from modules.nimovman.core import config,util
#from modules.nimovman.xui.core import GuiRegister,GuiRegisterUpdate






@util.onlyone
class PluginLoader(object):
    def __init__(self):
        self.__name="PluginLoader"
        self.plugins_path=config.C_PLUGIN_PATH
        self.user_plugins_path=config.C_USER_PLUGIN_PATH
        
        self.plugins=util.get_plugins(self.plugins_path)
        self.user_plugins=util.get_plugins(self.user_plugins_path)
        

        self.__plugins_dict_gui={}
        self.__plugins_dict_nongui={}


        self.__loaded_plugins_dict_gui={}
        self.__loaded_plugins_dict_nongui={}
    
    
    def load_user_plugins(self):pass

    def load_plugins(self):
        Log(self.__name).info("Loading all alvailable plugins: %s",self.plugins)
        for plugin in self.plugins:
            try:
                loaded_plugin=self.load_plugin(plugin)
                #Log("__________").info(loaded_plugin)
                #print loaded_plugin
                try:
                    try:exec("self.__loaded_plugins_dict_gui['%s']=loaded_plugin.%s.Plugin()"%(plugin,plugin))
                    except:
                        self.__loaded_plugins_dict_gui[plugin]=loaded_plugin.Plugin()
                        
                    #print dir(loaded_plugin)
                    #Log("PLUGIN_DIR").info("Plugin Loaded: %s",dir(loaded_plugin))
                    Log(self.__name).info("Plugin Loaded: %s",plugin)
                except Exception,e:
                    Log(self.__name).critical("Inside plugin Load dict %s - %s",e,error())
            except Exception,e:
                Log(self.__name).critical("Inside load Plugin Loop: %s - %s",e,error())
            
                
    def load_plugin(self,name):
        #print "Plugin Type",self.get_plugin_type(name)
        Log(self.__name).info("Loading plugin: %s",name)
        plugin="plugins.%s"%name
        if self.get_plugin_type(name)=="gui":
            #print plugin
            try:self.__plugins_dict_gui[name]=__import__(plugin)
            except:self.__plugins_dict_gui[name]=__import__(name)
            #self.__plugins_dict_gui[name]=__import__('modules.plugins.%s'%name, globals(), locals(), ["Plugin"], -1)
            return self.__plugins_dict_gui[name]
        elif self.get_plugin_type(name)=="nongui":
            try:self.__plugins_dict_nongui[name]=__import__(plugin)
            except:self.__plugins_dict_nongui[name]=__import__(name)
            return self.__plugins_dict_nongui[name]
            
    
    def unload_plugin(self,name):
        if self.get_plugin_type(name)=="gui":
            rname=self.__plugins_dict_gui[name]
            del self.__plugins_dict_gui[name]
            return rname
        elif self.get_plugin_type(name)=="nongui":
            rname=self.__plugins_dict_nongui[name]
            del self.__plugins_dict_nongui[name]
            return rname
    
    def get_plugin_module(self,name):
        if self.get_plugin_type(name)=="gui":return self.__plugins_dict_gui[name]
        elif self.get_plugin_type(name)=="nongui":return self.__plugins_dict_nongui[name]
    
    def get_plugin_instance(self,name):
        if self.get_plugin_type(name)=="gui":return self.__loaded_plugins_dict_gui[name]
        elif self.get_plugin_type(name)=="nongui":return self.__loaded__plugins_dict_nongui[name]
    
    
    def get_plugin_type(self,name):
        #has_plugin=False
        wplugin=None
        try:
            self.plugins.index(name)
            #has_plugin=True
            wplugin=os.path.join(self.plugins_path,name,"imovman-plugin")
        except:
            try:
                self.user_plugins.index(name)
                wplugin=os.path.join(self.user_plugins_path,name)
                #has_plugin=True
            except:pass
        if wplugin!=None:
            plugin_info=util.form_dict(wplugin)
            if plugin_info.has_key("plugin-type"):
                return plugin_info["plugin-type"].lower()

    def get_plugin_info(self,name):
        #has_plugin=False
        wplugin=None
        try:
            self.plugins.index(name)
            #has_plugin=True
            wplugin=os.path.join(self.plugins_path,name,"imovman-plugin")
        except:
            try:
                self.user_plugins.index(name)
                wplugin=os.path.join(self.user_plugins_path,name)
                #has_plugin=True
            except:pass
        if wplugin!=None:
            plugin_info=util.form_dict(wplugin)
            return plugin_info
        return {}
        
    def Instance(self):return self

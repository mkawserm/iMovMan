'''
Created on May 18, 2013

@author: KaWsEr
'''
import os
import idb
import ast
import json
import bottle
import cherrypy


import utility
from jinja2 import Environment, FileSystemLoader
import urllib, mimetypes




import webuid

















######################################################
class UiConfig(object):
    def __init__(self):
        self.cnf=idb.CDb().all()
        self.theme=ast.literal_eval(self.cnf["active_theme"])
        self.theme_path=ast.literal_eval(self.cnf["theme_path"])+"/"+self.theme
        self.tpl=os.path.realpath(os.path.join(self.theme_path,"index.html"))
        self.env = Environment(loader=FileSystemLoader(self.theme_path))
        
        self.index = self.env.get_template('index.html')
        
        self.aidb=idb.IDb()
        

######

def mimetype(typ):
    def decorate(func):
        def wrapper(*args, **kwargs):
            cherrypy.response.headers['Content-Type'] = typ
            return func(*args, **kwargs)
        return wrapper
    return decorate


class Cover(object):
    def default(self,path):
        q=path
        print q
        if q:
            try:
                k=bottle.static_file(os.path.basename(unicode(q)),os.path.dirname(unicode(q)))
                return k
            except:
                return None
        else:
            return None
    default.exposed=True
    

class Root(object):
    #_cp_config = {'tools.gzip.on': True}
    def __init__(self):
        self.uic=UiConfig()
        self.idb=idb.IDb()
        self.usb_data=""
        
        
    #############################################    
    def index(self,**query):return self.uic.index.render()
    index.exposed=True
    
    
    
    
    def load_movies(self,**query):
        #term=self.request.query.get ('term')
        term=""
        if query.has_key("term"):
            term=query["term"]
            
        #######    
        data=""
        if term!="all":
            data=self.idb.search_movies(tag=term)
        else:data=self.idb.search_movies()
        return data
    load_movies.exposed=True
    
    
    def usb_updates(self):
        try:
            data=utility.get_drives()
            if data!=self.usb_data:
                self.usb_data=data
                return json.dumps(["1"])
            else:return json.dumps(["0"])
        except Exception,e:
            print e
            return json.dumps(["0"])
    usb_updates.exposed=True
    
    def get_drives(self):
        #print "Request To get Drives..."
        lst=utility.get_drive_details()
        new_lst={}
        for i in lst:new_lst[i[0]]={"name":i[1]+" ("+i[0].replace("\\","")+")","path":i[0]}
        js=json.dumps(new_lst)
        return js
    get_drives.exposed=True
    
    def cover(self,path,**query):
        #q=path
        #print q
        url = urllib.pathname2url(path)
        ct=mimetypes.guess_type(url)[0]
        #print ct
        
        try:
            cherrypy.response.headers['Content-Type']= ct
            #print path
            fp=open(unicode(path),"rb")
            data=fp.read()
            fp.close()
            return data
        except:return None
    cover.exposed=True
################################################


##########################The Server##########################
class CherryPyServer(object):
    def __init__(self):
        self.host="127.0.0.1"
        self.port=9090
        self.bottle=True
        
        self.ui=UiConfig()
        self.cnf=self.ui.cnf
        
        self.theme_name=ast.literal_eval(self.cnf["active_theme"])
        self.theme_dir=ast.literal_eval(self.cnf["theme_path"])
                                    
        self.theme_path=os.path.realpath( os.path.join( ast.literal_eval(self.cnf["theme_path"]) , ast.literal_eval(self.cnf["active_theme"])) )
        

        self.static=[]
        #self.static=["aristo","image","img","isrc","jquery","src","static",self.theme_name]
        dirs=os.listdir(self.theme_path)
        for i in dirs:self.static.append(i)
        #self.static=[self.theme_name]
        
        self.site_name="http://"+self.host+":"+str(self.port)+"/"
    def prun(self):
        
        #cherrypy.engine.autoreload.
        #cherrypy.engine.autoreload.on = False
        favicon_path=os.path.abspath(os.path.realpath(os.path.join(self.theme_path,"favicon.ico")))
        #print favicon_path
        #print os.path.exists(favicon_path)
        
        conf={
              'server.socket_host': self.host,
              'server.socket_port':self.port,
              'server.thread_pool': 20,
              'tools.sessions.on' : True,
              'log.screen': False
              }
        

        
        
        """
        global_conf = {'global': {
                                  'server.socket_host': 'localhost',
                                  'server.socket_port': 8080,
                                  },
                       }
        
        app_conf={
                  '/favicon.ico':{
                                  'tools.staticfile.on':True,
                                  'tools.staticfile.filename':favicon_path}
                  }

        application_conf = {
                            '/style.css': {
                                           'tools.staticfile.on': True,
                                           'tools.staticfile.filename': os.path.join(_curdir,'style.css'),
                                           }
                            }
        """
        
        cherrypy.response.stream=True
        cherrypy.engine.timeout_monitor.unsubscribe()
        cherrypy.engine.autoreload.unsubscribe()
        cherrypy.config.update(conf)
        #cherrypy.config.update({"tools.sessions.on": True})
        #cherrypy.tools.staticfile.on = True
        #cherrypy.tools.staticfile.filename = os.path.join(self.theme_path,"favicon.ico")
        
        for i in self.static:
            cherrypy.tree.mount(None, '/%s'%i, {'/' : {'tools.staticdir.dir': u"%s/%s"%(self.theme_path,i),'tools.staticdir.on': True,} } )
        
        if os.path.exists(favicon_path):
            cherrypy.tree.mount(None, '/favicon.ico', {'/' : {'tools.staticfile.filename': u"%s"%(favicon_path),'tools.staticfile.on': True,} } )
        
        
        
        

        #####Bootle####
        if self.bottle:
            cherrypy.tree.graft(webuid.WebUi().app, '/')#it is used to call wsgi
        else:
            config = {'/':{
                           #'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                           'tools.trailing_slash.on': False,
                           }
                      }
            root=Root()
            cherrypy.tree.mount(root, "/",config=config)
        ##### ENd of bottle#####
        
        """

        """
        
        cherrypy.engine.start()
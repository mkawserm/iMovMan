#!/usr/bin/env python




import os
import ast
import idb
import json
import bottle
import utility
#import crawler
import config
from bottle import jinja2_template as template,request





class WebUi(object):
    def __init__(self):
        self.cdb=idb.CDb()
        self.idb=idb.IDb()
        self.app=self.app_one_def()
    
    
    def app_one_def(self):
        app=bottle.Bottle()
        cnf=idb.CDb().all()
        try:
            theme=ast.literal_eval(cnf["active_theme"])
            theme_dir=ast.literal_eval(cnf["theme_path"])
        except:
            theme=config.C_DEFAULT_THEME
            theme_dir=config.C_THEME_PATH
        theme_path=theme_dir+"/"+theme
        tpl=os.path.realpath(os.path.join(theme_path,"index.html"))
        aidb=idb.IDb()
        
        
        """
        ## All Static File Server ##
        @app.route('<path:path>')
        def all_static(path):
            print "Seriving static...",path
            if not path.endswith("html"):return bottle.static_file( os.path.basename(unicode(path)),unicode(theme_path)+os.path.dirname(unicode(path)) )
            else:return ""
        """
        
        self.usb_data="" 
        ### Open Api Json Server ####
        @app.route('/oapi<path:path>')
        def oapi(path):
            #plist=path.split("::")
            #add #update #load #delete #open #send
            action=request.query.get ('a')#action
            name=request.query.get ('n')#name
            opt=request.query.get('o')#it is a python dictionary
            
            mopt={}
            try:
                oplist=opt.split("::")
                for i in oplist:
                    il=i.split(":-")
                    mopt[il[0]]=il[1]
            except:mopt={}
            #print action
            #print opt
            #print name
            #print opt
            
            if action=="update" and name=="wstatus":
                print "oapi Updating wstatus....",mopt
                if mopt.has_key("wstatus") and mopt.has_key("path"):
                    if aidb.update_wstatus(mopt["path"],mopt["wstatus"]):
                        return json.dumps(["1"])
                    else:return json.dumps(["0"])
            
            if action=="open" and name=="run_movie":
                print "oapi Running Movie ",mopt
                if mopt.has_key("path"):
                    print mopt
                    if utility.default_file_open(mopt["path"]):return json.dumps(["1"])
                    else:return json.dumps(["0"])
            
            if action=="load" and name=="get_drives":
                print "oapi get_drives"
                lst=utility.get_drive_details()
                new_lst={}
                for i in lst:new_lst[i[0]]={"name":i[1]+" ("+i[0].replace("\\","")+")","path":i[0]}
                js=json.dumps(new_lst)
                return js
            
            if action=="update" and name=="usb_updates":
                
                try:
                    data=utility.get_drives()
                    if data!=self.usb_data:
                        print "oapi usb_updates"
                        self.usb_data=data
                        return json.dumps(["1"])
                    else:return json.dumps(["0"])
                except Exception,e:
                    print e
                    return json.dumps(["0"])
                
            if action=="open" and name=="open_folder":
                print "oapi open_folder"
                if mopt.has_key("path"):
                    dname=os.path.dirname(mopt["path"])
                    if utility.open_folder(unicode(dname)):return json.dumps(["1"])
                    else:return json.dumps(["0"])
                else:return json.dumps(["0"])
            
            if action=="send" and name=="send_to":
                print "opai send_to"
                if mopt.has_key("src") and mopt.has_key("dst"):
                    src=mopt["src"]
                    dst=mopt["dst"]
                    try:
                        src=unicode(src)
                        dst=unicode(dst)
                        utility.default_file_copy(src,dst)
                        return json.dumps(["1"])
                    except Exception,e:
                        print e
                        return json.dumps(["0"])
                else:return json.dumps(["0"])
                
            if action=="send" and name=="send_to_folder":
                print "opai send_to_folder"
                if mopt.has_key("src") and mopt.has_key("dst"):
                    src=mopt["src"]
                    dst=mopt["dst"]
                    try:
                        src=unicode(os.path.dirname(src))
                        dst=unicode(dst)
                        utility.default_file_copy(src,dst)
                        return json.dumps(["1"])
                    except Exception,e:
                        print e
                        return json.dumps(["0"])
                else:return json.dumps(["0"])
            if action=="load" and name=="load_movies":
                print "oapi load_movies"
                term=""
                if mopt.has_key("term"):term=mopt["term"]
                data=""
                if term!="all":data=aidb.search_movies(tag=term)
                else:data=aidb.load_movies_all()
                return data
            
            if action=="load" and name=="watched_movies":
                print "oapi watched_movies"
                data=aidb.load_watched_movies()
                return data
            if action=="load" and name=="notwatched_movies":
                print "oapi Not watched_movies"
                data=aidb.load_notwatched_movies()
                return data
            if action=="load" and name=="wanttowatch_movies":
                print "oapi Not watched_movies"
                data=aidb.load_wanttowatch_movies()
                return data
            if action=="load" and name=="sort_rating":
                print "Sorting By Rating"
                data=aidb.sort_by_rating()
                return data
            if action=="load" and name=="sort_year":
                print "Sorting By Rating"
                data=aidb.sort_by_year()
                return data
            if action=="load" and name=="get_genres":
                return aidb.get_genres()   
                
                
        
        
        
    
            

        
        
        
        ## Cover Server ##
        @app.route('/cover/<path:path>')
        def cover(path):
            q=path
            if q:return bottle.static_file(os.path.basename(unicode(q)),os.path.dirname(unicode(q)))
            else:return None
        """
        @app.route('<path:path>')
        def all_static(path):
            if not path.endswith("html"):
                return bottle.static_file( os.path.basename(unicode(path)),unicode(theme_path)+os.path.dirname(unicode(path)) )
            else:return ""
        """
            
        
        """search Server"""
        @app.route('/api')
        def iapi_panel():
            q=request.query.get ('q')
            #fake=[]
            if q:
                q=unicode(q)
                job=unicode(request.query.get ('job'))
                if job==u"search":
                    stype=unicode(request.query.get ('stype'))
                    if stype==u"all":
                        #print "requesting ...",q
                        #sapi=iapi.SearchApi()
                        json_data=aidb.get_tags(tag=q)
                        #print json_data
                        if len(json_data)>0:
                            return json_data
                elif job==u"movie":
                    print job
                    imdbid=unicode(request.query.get("imdbid"))
                    print imdbid
                    if imdbid:
                        return aidb.get_movie_by_imdbid(imdbid)
                elif job==u"stat":
                    return aidb.get_stat()
        
        
        
        
        
        

   
        
        
        @app.route('/run_movie')
        def run_movie():
            q=request.query.get ('q')
            if q:
                if utility.default_file_open(q):return json.dumps(["1"])
                else:return json.dumps(["0"])
            else:return json.dumps(["0"])
        
        
        
        @app.route('/get_drives')
        def get_drives():
            print "Request To get Drives..."
            lst=utility.get_drive_details()
            new_lst={}
            for i in lst:new_lst[i[0]]={"name":i[1]+" ("+i[0].replace("\\","")+")","path":i[0]}
            js=json.dumps(new_lst)
            return js
        
        
        
        
        self.usb_data="" 
        @app.route('/usb_updates')
        def usb_updates():
            try:
                data=utility.get_drives()
                if data!=self.usb_data:
                    self.usb_data=data
                    return json.dumps(["1"])
                else:return json.dumps(["0"])
            except Exception,e:
                print e
                return json.dumps(["0"])
            
        """Open Folder"""
        @app.route('/open_folder')
        def open_folder():
            q=request.query.get ('q')
            if q:
                dname=os.path.dirname(q)
                print "Opening..",dname
                if utility.open_folder(unicode(dname)):return json.dumps(["1"])
                else:return json.dumps(["0"])
            else:return json.dumps(["0"])
        
        
        
        """Send To only File"""
        @app.route('/send_to')
        def send_to():
            print "Send To initiated..."
            src=request.query.get ('src')
            dst=request.query.get ('dst')
            if src and dst:
                try:
                    src=unicode(src)
                    dst=unicode(dst)
                    utility.default_file_copy(src,dst)
                    return json.dumps(["1"])
                except Exception,e:
                    print e
                    return json.dumps(["0"])
            else:return json.dumps(["0"])
        
            
        """Send To Full Folder"""
        @app.route('/send_to_folder')
        def send_to_folder():
            print "Send To initiated..."
            src=request.query.get ('src')
            dst=request.query.get ('dst')
            if src and dst:
                try:
                    d=os.path.dirname(src)
                    src=unicode(d)
                    dst=unicode(dst)
                    utility.default_file_copy(src,dst)
                    return json.dumps(["1"])
                except Exception,e:
                    print e
                    return json.dumps(["0"])
            else:return json.dumps(["0"])    
        
        
        
        
        
        
        @app.route('/load_movies')
        def load_movies():
            term=request.query.get ('term')
            data=""
            if term!="all":
                data=aidb.search_movies(tag=term)
            else:data=aidb.search_movies()
            return data
        
        """Get Genres"""
        @app.route('/get_genres')
        def get_genres():return aidb.get_genres()
        
        
        
        @app.route("/")
        @app.route('/<anything:path>')
        def page(anything=None):
            #print anything
            info={}
            return template(tpl,info=info)
        
        

        return app
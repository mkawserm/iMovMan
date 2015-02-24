'''
Created on Jul 18, 2013

@author: KaWsEr
'''

import config


import re
import os
import sys
import ast
import bs4
#import util
import json


import inspect
import urllib2
#import threading
import traceback
import threading
import datetime
import time
import codecs
from urllib import quote_plus
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from modules.nimovman.core import Log
from modules.nimovman.core.util import next_time
from modules.nimovman.core import standardsignal

#from modules.nimovman.core.dbmodel import MovieDbModel,MetaDbModel,TrashDbModel

from dbmodel import Option,Movie,MovieModel,Trash

#from PySide import QtGui,QtCore
import util

###############

####################################
def get_imdbid(url):
    imdbid=url.split("/")
    mimdbid=None
    for i in imdbid:
        if i.find("tt")==0:
            mimdbid=i
            break
    #print "Mimdbid: ",mimdbid
    return mimdbid
##### x ##################

def get_patterns():
    #opt_patterns=[]
    try:cdb=Option()
    except:pass
    try:opt_patterns=cdb.get_option("opt_patterns")
    except:pass
    if opt_patterns==None:opt_patterns=[]
    return opt_patterns

#######################

####################################
def getgoogleurl(search,siteurl=False):
    #return 'http://www.google.com/search?q='+urllib2.quote(search)+'&oq='+urllib2.quote(search)
    if siteurl==False:
        return 'http://www.google.com/search?q='+quote_plus(search.encode('utf8'), safe='/')+'&oq='+quote_plus(search.encode('utf8'), safe='/')
    else:
        return 'http://www.google.com/search?q=site:'+quote_plus(siteurl.encode('utf8'), safe='/')+'%20'+quote_plus(search.encode('utf8'), safe='/')+'&oq=site:'+quote_plus(siteurl.encode('utf8'), safe='/')+'%20'+quote_plus(search.encode('utf8'), safe='/')

def getgooglelinks(search,siteurl=False):
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'}
    data=""
    try:
        req = urllib2.Request(getgoogleurl(search,siteurl),None,headers)
        site = urllib2.urlopen(req)
        data = site.read()
        site.close()
    except:pass
    soup = bs4.BeautifulSoup(data)
    #print soup.title
    links=[]
    for link in soup.find_all('a'):
        href=link.get('href')
        if href!=None:
            if href.find("title/tt")!=-1:
                links.append(href)
                #print href,"\n"
    if len(links)==0:return False
    return links
###################################################

def get_smartest_name(name):
    patterns=[r'^(.*) \(([1-2][0-9][0-9][0-9])\)',
              r'^(.*) ([1-2][0-9][0-9][0-9])',
              r'^(.*)\.([1-2][0-9][0-9][0-9])',
              r'^(.*) .*([1-2][0-9][0-9][0-9])']
    
    patterns=patterns+get_patterns()
    
    for pattern in patterns:
        title=None
        year=None
        try:
            matchObj = re.match(pattern,name, re.M|re.I)
            if matchObj:
                title=matchObj.group(1)
                year=matchObj.group(2)
                break
        except:pass
    return title,year
        





####################################################
def error():
    """TraceBack Error"""
    for frame in traceback.extract_tb(sys.exc_info()[2]):
        fname,lineno,fn,text = frame
        estr="[%s:%d] - Error:%s" % ("function ("+fn+") :: "+fname,lineno,text)
        #print estr
        return estr
##########################################


class MovieUpdater(threading.Thread):
    MovieUpdaterStarted=standardsignal.SignalBool()
    MovieUpdaterFinished=standardsignal.SignalBool()
    MovieUpdaterUpdates=standardsignal.SignalUnicode()
    MovieUpdaterGenreUpdated=standardsignal.Signal()
    MovieUpdaterYearUpdated=standardsignal.Signal()
    def __init__(self,imd):
        super(MovieUpdater,self).__init__()
        self.setDaemon(True)
        self.__name="MovieUpdater"
        self.setName(self.__name)
        self.imd=imd
        self.loop=True
        self.loops=0
        self.engage_time=5
        self.one_out=True
        self.first_time=time.clock()
        self.notify_timer=time.clock()
        self.notify_timeout=3*60
        self.movie=Movie()
        self.option=Option()

    
    def run(self):
        while self.loop:
            etime=int(time.clock()-self.first_time)
            ntime=int(time.clock()-self.notify_timer)
            if etime>=self.engage_time:
                if self.one_out:
                    Log(self.__name).info("%s Engaged :%s",self.__name,etime)
                    self.one_out=False
                self.updater()
            if ntime==self.notify_timeout:
                now=datetime.datetime.now().time()
                next_call=next_time(now,self.notify_timeout)
                self.notify_timer=time.clock()
                Log(self.__name).info("%s completed %s loops %s next call @%s",self.__name,self.loops,ntime,next_call)
                #time.sleep(3)
                #os.wa
            self.loops=self.loops+1
            time.sleep(1)
            #print self.loops
            #break


    def __helper_cover_data(self):
        try:data_dir=Option().get_option("data_dir")
        except Exception,e:
            Log(self.__name).error("Data Directory Not Found %s-%s",e,error())
            #self.notify("Data Directory Not Found")
            return False
        try:cover_dir=Option().get_option("cover_dir")
        except:
            Log(self.__name).error("Cover Directory Not Found")
            #self.notify("")
            return False
        
        try:data_dir_index=config.DATA_DIR.index(data_dir)
        except Exception,e:
            Log(self.__name).error("%s-%s",e,error())
            data_dir_index=0
        try:cover_dir_index=config.DATA_DIR.index(cover_dir)
        except:cover_dir_index=0
        
        #print data_dir_index,cover_dir_index
        data_path=None
        if data_dir_index==1:
            data_path=config.C_DATA_PATH     
        elif data_dir_index==2:
            try:data_path=Option().get_option("data_dir_custom")
            except:
                #data_path=False
                Log(self.__name).error("Custom Data Directory Not Found %s",error())
                #self.notify("Custom Data Directory Not Found")
                return False
            
        cover_path=None
        if cover_dir_index==1:
            cover_path=config.C_COVER_PATH
        elif cover_dir_index==2:
            try:cover_path=Option().get_option("cover_dir_custom")
            except:
                #data_path=False
                Log(self.__name).critical("Custom Cover Directory Not Found %s",error())
                return False
        return (data_path,cover_path)

    def logic_one(self,name):pass
    



    
    def updater(self):
        try:MovieUpdater.MovieUpdaterStarted.signal.emit(True)
        except:Log(self.__name).critical("Signal Sending Error %s",error())
        try:data_path,cover_path=self.__helper_cover_data()
        except:return False
        if data_path!=None:self.make_dirs(data_path)
        if cover_path!=None:self.make_dirs(cover_path)

        try:self.api=self.option.get_option("movie_api")
        except:self.api=config.C_DEFAULT_API
        
        
        try:
            try:
                #print self.api
                #print sys.path
                mapi=__import__(self.api)
                #print mapi
                obj_mapi=mapi.mApi()
            except Exception,e:
                Log(self.__name).debug("API Loading Failed %s %s",error(),e)
                sys.exit(0)
            #try:
            #except:obj_mapi=None
            #print obj_mapi
            if obj_mapi!=None:
                movies=self.movie.get(i=1).filter(MovieModel.imdbid==u"").all()
                for smovie in movies:
                    #print smovie.path
                    movie_name=""
                    movie_name_wext=os.path.basename(smovie.path)
                    movie_name=self.name_without_ext(movie_name_wext)
                    idata_path=""
                    icover_path=""
                    #print movie_name
                    #print "DataPath",data_path
                    if data_path==None:
                        idata_path=os.path.dirname(smovie.path)
                        idata_path=os.path.join(idata_path,movie_name)
                    else:
                        idata_path=os.path.join(data_path,movie_name)
                        
                    if cover_path==None:
                        icover_path=os.path.dirname(smovie.path)
                        icover_path=os.path.join(icover_path,movie_name)
                    else:
                        icover_path=os.path.join(cover_path,movie_name)
                        
                    #print "Data",data_path
                    
                    
                    
                    idata_path_old=idata_path+".txt"
                    idata_path_new=idata_path+config.EXT_TXT
                    
                    try:cover_format=self.option.get_option("C_COVER_FORMAT")
                    except:cover_format=config.C_COVER_FORMAT
                    #cp=cover_path
                    cfound=False
                    for cf in cover_format:
                        cp=icover_path+"."+cf.lower()
                        #print cp
                        if os.path.exists(cp):
                            cfound=True
                            break
                    data=None
                    #"""    
                    if os.path.exists(idata_path_old):
                        data=self.form_dict(idata_path_old)
                        try:os.remove(idata_path_old)
                        except:pass
                    
                    if data==None:
                        if os.path.exists(idata_path_new):
                            data=self.form_dict(idata_path_new)
                    else:
                        if not os.path.exists(idata_path_new):
                            self.make_txt(data, idata_path_new)
                    
                    if data==None:
                        #print data,cfound,data_path_new
                        #print cover_path,data_path
                        title,year=get_smartest_name(movie_name)
                        #print title,year
                        if title!=None and year!=None:
                            try:data=obj_mapi.get(t=title,y=year)
                            except:data=None
                        
                        elif title!=None and year==None:
                            try:data=obj_mapi.get(t=title)
                            except:data=None
                    
                    #Searching Logic#
                    if data==None:
                        sdata=None
                        if title!=None and year!=None:
                            try:sdata=obj_mapi.search(s=title,y=year)
                            except:sdata=None
                        elif title!=None and year==None:
                            try:sdata=obj_mapi.search(s=title)
                            except:sdata=None
                        
                        if type(sdata)==list:
                            #print sdata
                            for isdata in sdata:
                                if type(isdata)==dict:
                                    #print "Dict Ok"
                                    if isdata.has_key("type"):
                                        if isdata["type"]==u"movie" or isdata["type"]==u"video":
                                            #print "Key Okeys"
                                            if isdata.has_key("imdbid"):
                                                try:
                                                    data=obj_mapi.get(i=isdata["imdbid"])
                                                    #print data
                                                    if type(data)==dict:#confused movies#
                                                        #If You Have Any Confusion Add it to database
                                                        break
                                                except:
                                                    data=None
                                        
                                         
                            #links = getgooglelinks(movie_name,'http://www.imdb.com')
                            #print links
                    #"""        
                    #print icover_path,idata_path_new#data
                    #print data
                    if type(data)==dict:
                        if not os.path.exists(idata_path_new):
                            self.make_txt(data,idata_path_new)
                        if cfound==False:
                            if data.has_key("poster"):
                                try:self.getCover(data["poster"], icover_path+".jpg")
                                except:pass
                        data=self.make_unique_dict(data)
                        #print data
                        data["path"]=smovie.path
                        #print smovie.path
                        
                        ###Genre Update Logic###
                        if data.has_key("genre"):
                            #Log(self.__name).info("Trying To Update Genres:")
                            genres=data["genre"]
                            genres=genres.split(",")
                            
                            try:
                                opt=Option()
                                old=opt.get_option("option_genre")
                            except:pass
                            if old==None:old=[]
                            
                            
                            genlist=[]
                            genreupdated=False
                            for sgenre in genres:
                                try:
                                    sgenre=sgenre.strip().lower()
                                    if sgenre not in old:
                                        genlist.append(sgenre)
                                        genreupdated=True
                                except Exception,e:
                                    Log(self.__name).critical("While Updating genre %s-%s",e,error())
                            ngenlist=old+genlist
                            try:

                                if genreupdated:
                                    Log(self.__name).info("Updating Genres")
                                    opt.replace("option_genre", ngenlist)
                                    Log(self.__name).info("Genres Updated")
                                    try:self.MovieUpdaterGenreUpdated.signal.emit()
                                    except Exception,e:Log(self.__name).critical("While Sending Signal %s-%s",e,error())
                            except Exception,e:
                                Log(self.__name).critical("While Updating genre %s-%s",e,error())
                        ## End of Genre Update Logic ##
                        
                        ## Year Update Logic ##
                        if data.has_key("year"):
                            try:
                                year=int(data["year"])
                                try:
                                    opt=Option()
                                    old=opt.get_option("option_year")
                                except:pass
                                if old==None:old=[]
                                yearupdated=False
                                if year not in old:
                                    old.append(year)
                                    yearupdated=True
                                try:
                                    if yearupdated:
                                        Log(self.__name).info("Updating Year")
                                        opt.replace("option_year", old)
                                        Log(self.__name).info("Year Updated")
                                        try:self.MovieUpdaterYearUpdated.signal.emit()
                                        except Exception,e:Log(self.__name).critical("While Sending Signal %s-%s",e,error())
                                except Exception,e:
                                    Log(self.__name).critical("While Updating year %s-%s",e,error())
                            except Exception,e:
                                Log(self.__name).critical("While Updating year %s-%s",e,error())
                        ## End of Year Update Logic ##
                            
                        
                        
                        ##Update Movie Data##    
                        if self.movie.update(data):#Data Updated Send The Notification
                            Log(self.__name).info("Movie Updated: "+movie_name_wext)
                            self.notify("Movie Updated: "+movie_name_wext)
                            try:MovieUpdater.MovieUpdaterUpdates.signal.emit(unicode(data["path"]))
                            except:Log(self.__name).critical("Signal Sending Error %s",error())
                    #break
                
        except Exception,e:
            Log(self.__name).error("%s-%s",e,error())
        try:MovieUpdater.MovieUpdaterFinished.signal.emit(True)
        except:Log(self.__name).critical("Signal Sending Error %s",error())
        #exit(0)
    
    def make_unique_dict(self,data):
        #print data
        ndata={}
        for i in data.keys():
            ndata[i.lower()]=data[i]
        return ndata
    def getCover(self,url,save_as):
        """Get The Movie Cover"""
        Log(self.__name).info("Downloading cover %s",url)
        f = urllib2.urlopen(url)
        with open(save_as,'wb') as output:
            while True:
                buf = f.read(65536)
                if not buf:break
                output.write(buf)
        Log(self.__name).info("Cover Downloaded %s",url)
                       
    def form_dict(self,path):
        """This Will Form the dictionary From the text data"""
        dkeys=config.MOVIE_DB_KEYS
        data={}
        try:
            f=codecs.open(path, "r", "utf-8")
            text=f.read()
            f.close()
        except Exception:text=None
        if text!=None:
            #print text
            lines=text.split("\n")
            for sline in lines:
                if sline!="" or sline==None:line_data=sline.partition(":")
                if len(line_data)==3:
                    try:
                        kin=dkeys.index(line_data[0].strip().decode("utf-8"))
                        data[dkeys[kin]]=line_data[2].strip()
                        data[dkeys[kin].lower()]=line_data[2].strip()
                    except:pass
        else:return None
        
        if data.has_key("Title"):
            if not data.has_key("Type"):
                data["Type"]=u"movie"
                data["type"]=u"movie"
        return data
    def make_txt(self,data,save_as):
        """This Will Create The Text Data"""
        Log(self.__name).info("Making Data: %s",save_as)
        dkeys=config.MOVIE_DB_KEYS
        if data:
            try:
                f=codecs.open(save_as, "w+", "utf-8")
                for i in dkeys:
                    if data.has_key(i):
                        f.write(i+": "+ data[i]+"\n")
                f.write("\n")
                f.write(u"SoftwareName: "+unicode(config.APP_NAME)+u"\n")
                f.write(u"SoftwareVersion: "+unicode(config.APP_VERSION)+u"\n")
                f.write(u"SoftwareDeveloper: "+unicode(config.APP_DEVELOPER)+u"\n")
                f.write(u"SoftwareHomepage: "+unicode(config.APP_WEB)+u"\n")
                f.write(u"CompanyHomepage: "+unicode("http://www.cliodin.com")+u"\n")
                f.write(u"FacebookHomepage: "+unicode("https://www.facebook.com/cliodin")+u"\n")                
                f.close()
                return True
            except Exception,e:
                Log(self.__name).critical("Exception occured while Making Data = %s-%s",e,error())
        return False


    def name_without_ext(self,name):
        return name.replace("."+name.split(".")[-1],"")
    
    def notify(self,msg):
        self.imd.add_msg(msg)
        
        
    def make_dirs(self,p):
        """make parent dirs"""
        if os.path.isfile(p):
            dn=os.path.dirname(p)
        else:dn=p
        if dn!="":
            if not os.path.exists(dn):
                os.makedirs(dn)
######################################



class MovieAdder(threading.Thread):
    MovieAdderStarted=standardsignal.SignalBool()
    MovieAdderFinished=standardsignal.SignalBool()
    MovieAdderUpdates=standardsignal.SignalUnicode()
    def __init__(self,imd):
        super(MovieAdder,self).__init__()
        self.setDaemon(True)
        self.__name="MovieAdder"
        self.setName(self.__name)
        self.imd=imd
        self.loop=True
        self.loops=0
        self.auto_scan_def()
        #self.auto_delete_def()
        self.engage_time=5#Seconds
        self.first_time=time.clock()
        self.one_out=True
    
    def is_auto_scan_enabled(self):
        try:
            index=config.EN_DIS.index(self.auto_scan)
            if index==0:return True
        except:pass
        return False
            
    def auto_scan_def(self):
        option=Option()
        self.auto_scan=config.EN_DIS[1]
        try:self.auto_scan=option.get_option("auto_scan")
        except Exception,e:print e

        
    def run(self):
        while self.loop:
            etime=int(time.clock()-self.first_time)
            if etime>=self.engage_time:
                if self.one_out:
                    self.one_out=False
                    Log(self.__name).info("%s Engaged :%s",self.__name,etime)
                try:
                    index=config.EN_DIS.index(self.auto_scan)
                    if index==0:self.scan()
                except Exception,e:
                    Log(self.__name).critical("Inside Loop: %s-%s",e,error())
            self.loops=self.loops+1
            time.sleep(1)
        
    def scan(self):
        try:MovieAdder.MovieAdderStarted.signal.emit(True)
        except:Log(self.__name).critical("Sending Signal Error :%s",error())
        try:
            option=Option()
            paths=option.get_option("movie_paths")
        except Exception,e:
            print e
            paths=[]
        try:mformat=option.get_option("C_MOVIE_FORMAT")
        except:mformat=config.C_MOVIE_FORMAT
        if paths==None:paths=[]
        #print paths
        for mdir in paths:#Loop Through All Movie's Folder
            if os.path.exists(mdir):#check if the folder exists or not
                for (path,dirs, files) in os.walk(mdir):#now walk through the folder
                    #dirs
                    for s_file in files:
                        movie_path=os.path.realpath(os.path.join(path, s_file))
                        for single_format in mformat:
                            if movie_path.lower().endswith(single_format.lower()):
                                try:
                                    movie=Movie()
                                    trash=Trash()
                                    data={"path":movie_path}
                                    if not movie.has_path(movie_path):
                                        if not trash.is_deleted(movie_path):
                                            if movie.add(data):
                                                #print movie_path
                                                try:MovieAdder.MovieAdderUpdates.signal.emit(unicode(data["path"]))
                                                except:Log(self.__name).critical("Sending Signal Failed:%s",error())
                                                self.imd.add_msg("Added: "+s_file)
                                                Log(self.__name).info("Added: %s",s_file)
                                    del movie,trash,data
                                except Exception,e:
                                    Log(self.__name).critical("%s-%s",e,error())
                                    #self.mainwindow.scanner.setText(str(e))
        try:MovieAdder.MovieAdderFinished.signal.emit(True)
        except:Log(self.__name).critical("Signal Sending Failed: %s",error())

class MovieRemover(threading.Thread):
    MovieRemoverStarted=standardsignal.SignalBool()
    MovieRemoverFinished=standardsignal.SignalBool()
    MovieRemoverUpdates=standardsignal.SignalUnicode()
    def __init__(self,imd):
        super(MovieRemover,self).__init__()
        self.setDaemon(True)
        self.__name="MovieRemover"
        self.setName(self.__name)
        self.imd=imd
        self.loop=True
        self.loops=0
        self.auto_delete_def()
        self.start_timer=time.clock()
        self.first_time=time.clock()
        self.engage_time=5#Engaged Time
        self.one_out=True
        
    def is_auto_delete_enabled(self):
        try:
            index=config.EN_DIS.index(self.auto_delete)
            if index==0:return True
        except:pass
        return False
    
    def auto_delete_def(self):
        option=Option()
        self.auto_delete=config.EN_DIS[1]
        try:self.auto_delete=option.get_option("auto_delete")
        except:pass

    def run(self):
        while self.loop:
            etime=int(time.clock()-self.first_time)
            if etime>=self.engage_time:
                if self.one_out:
                    self.one_out=False
                    Log(self.__name).info("%s Engaged :%s",self.__name,etime)
                try:
                    index=config.EN_DIS.index(self.auto_delete)
                    if index==0:self.delete()
                except Exception,e:
                    Log(self.__name).critical("Inside Loop: %s-%s",e,error())
            self.loops=self.loops+1
            time.sleep(1)
            #break
            #print self.loops    
    
    def delete(self):
        try:MovieRemover.MovieRemoverStarted.signal.emit(True)
        except:Log(self.__name).critical("Signal Sending Failed %s",error())
        try:
            mo=Movie()
            movies=mo.get()
            for movie in movies:
                if  not os.path.exists(movie.path):
                    try:
                        name=movie.path.split("\\")[-1]
                        if mo.delete(movie.path):
                            try:MovieRemover.MovieRemoverUpdates.signal.emit(movie.path)
                            except:Log(self.__name).critical("Signal Sending Failed %s",error())
                            self.imd.add_msg("Removed: "+name)
                            Log(self.__name).info("Removed: %s",name)
                    except Exception,e:
                        print e

            if (time.clock()-self.start_timer)>=60*10:
                self.start_timer=time.clock()
                Log(self.__name).info("Optimizing Movies Database")
                try:
                    mo.v()
                    Log(self.__name).info("Movies Database optimized")
                except Exception,e:
                    Log(self.__name).critical("Exception occured while optimizing Database %s-%s",e,error())
        except Exception,e:
            Log(self.__name).critical("Movie Deleting Failed %s-%s",e,error())
        try:MovieRemover.MovieRemoverFinished.signal.emit(True)
        except:Log(self.__name).critical("Signal Sending Failed %s",error())
            

class IMd(object):
    obj=None
    def __init__(self,mainwindow):
        self.mainwindow=mainwindow
        #self.movie=Movie()
        #self.option=Option()
        self.trash=Trash()
        self.movie_adder=MovieAdder(self)
        self.movie_adder.start()
        self.movie_remover=MovieRemover(self)
        self.movie_remover.start()
        self.movie_updater=MovieUpdater(self)
        self.movie_updater.start()
        self.obj=self
    def add_msg(self,msg):
        self.mainwindow.StatusSignal.signal.emit(msg)
    
    @staticmethod
    def Instance():
        return IMd.obj
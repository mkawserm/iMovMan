#!/usr/bin/env python


"""
Created on May 14, 2013

@author: KaWsEr
"""




import re
import os
import sys
import ast
import codecs
import inspect
import datetime
import traceback
import bs4
#import threading
import operator

import config

###Used By OmdbApi####
import json
import urllib2
from urllib import quote_plus
#############################


from sqlalchemy import or_
######## Used By MyDbManager ########
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
########################################


######## Used By Db Models ###############
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,Float,Unicode,DateTime
###############################################################################

## Own Module ##
import utility



################### Global Variable ##### Application Configuration ###############################
APP_NAME=config.APP_NAME
APP_DEVELOPER=config.APP_DEVELOPER
APP_DEVELOPER_INFO=config.APP_DEVELOPER_INFO
APP_VERSION=config.APP_VERSION
APP_WEB=config.APP_WEB
APP_WEB_LABEL=config.APP_WEB_LABEL
APP_DESCRIPTION=config.APP_DESCRIPTION
APP_COPYRIGHT=config.APP_COPYRIGHT
#####################################





def icon(ic=None):
    #Icons#
    icon={}
    icon["imovman-32x32"]="data/png/imovman-32x32.png"
    icon["imovman-512x512"]="data/png/imovman-512x512.png"
    if ic==None:return icon
    else:
        if icon.has_key(ic):return icon[ic]
        else:return None
    


#########################################################################################
def getAppDetails():
    global APP_NAME,APP_DEVELOPER,APP_VERSION,APP_DESCRIPTION,APP_WEB,APP_WEB_LABEL,APP_COPYRIGHT
    return [APP_NAME,APP_DEVELOPER,APP_VERSION,APP_DESCRIPTION,APP_WEB,APP_WEB_LABEL,APP_COPYRIGHT]

#########################################################################################

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
#######################
def get_smart_name(name):
    name=name.replace("1080p","").replace("720p","").replace("."," ").strip()
    pattern1=r'^(.*) \(([1-2][0-9][0-9][0-9])\)'
    pattern2=r'^(.*) ([1-2][0-9][0-9][0-9])'
    pattern3=r'^(.*)\.([1-2][0-9][0-9][0-9])'
    pattern4=r'^(.*) .*([1-2][0-9][0-9][0-9])'
    title=None
    year=None
    try:
        matchObj = re.match(pattern1,name, re.M|re.I)
        if matchObj:
            title=matchObj.group(1)
            year=matchObj.group(2)
        else:
            matchObj = re.match(pattern2,name, re.M|re.I)
            if matchObj:
                title=matchObj.group(1)
                year=matchObj.group(2)
            else:
                matchObj = re.match(pattern3,name, re.M|re.I)
                if matchObj:
                    title=matchObj.group(1)
                    year=matchObj.group(2)
                else:
                    print "In Pattern 4"
                    matchObj=re.match(pattern4,name,re.M|re.I)
                    if matchObj:
                        title=matchObj.group(1)
                        year=matchObj.group(2)
                    else:
                        title=name
            if title!=None:
                title=title.replace("."," ").strip()
            return title,year
    except Exception,e:
        print e
        return title,year
    return title,year
####################################
def getgoogleurl(search,siteurl=False):
    #return 'http://www.google.com/search?q='+urllib2.quote(search)+'&oq='+urllib2.quote(search)
    if siteurl==False:
        return 'http://www.google.com/search?q='+urllib2.quote(search)+'&oq='+urllib2.quote(search)
    else:
        return 'http://www.google.com/search?q=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)+'&oq=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)

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
###################################





##############
############### Some UseFul Function #########################
def error():
    """TraceBack Error"""
    for frame in traceback.extract_tb(sys.exc_info()[2]):
        fname,lineno,fn,text = frame
        estr="[%s:%d] - Error:%s" % ("function ("+fn+") :: "+fname,lineno,text)
        #print estr
        return estr


def my_error(e):
    """TraceBack Error"""
    for frame in traceback.extract_tb(sys.exc_info()[2]):
        fname,lineno,fn,text = frame
        estr="[%s:%d] - Error:%s" % ("function ("+fn+") :: "+fname,lineno,text)
        estr=estr+" < "+str(e)+" >"
        #print estr
        return estr



#### ENd  #######






################################# dbhelper ##############################


def whoami():return inspect.stack()[1][3]



class MyDbManagerException(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)


class NoDataBaseDefined(MyDbManagerException):pass
class NoModelDefined(MyDbManagerException):pass
class NoEngineDefined(MyDbManagerException):pass
class NoSessionDefined(MyDbManagerException):pass
class UnknownError(MyDbManagerException):pass


class MyDbManager(object):
    """MyDbManager is a sqllite database helper class for Sqlalchemy"""
    def __init__(self,**kwargs):
        self.__db=None
        self.echo=False
        self.autoflash=False
        self.autocommit=False
        self.__engine=None
        self.__model=None
        self.__session=None
        if kwargs.has_key("db"):
            self.set_db(self.__db,**kwargs)
        if kwargs.has_key("model"):
            self.__model=kwargs["model"]
            self.set_model(self.__model,**kwargs)
    def set_db(self,idb,**kwargs):
        """Alias of setDb"""
        self.setDb(idb,**kwargs)
    def setDB(self,idb,**kwargs):
        """Alias of setDb"""
        self.setDb(idb,**kwargs)
    
    
    def setDb(self,idb,**kwargs):
        """Set The database"""
        self.__db=idb
        if kwargs.has_key("db"):
            self.__db=kwargs["db"]
            self.make_dirs(self.__db)
            self.__engine=create_engine('sqlite:///'+self.__db, echo=self.echo)
            if self.__session==None:
                self.__s__()
        elif self.__db!=None:
            self.make_dirs(self.__db)
            self.__engine=create_engine('sqlite:///'+self.__db, echo=self.echo)
            if self.__session==None:
                self.__s__()
        elif self.__db==None:
            raise NoDataBaseDefined("You have not provided any Database. example: object.s(db='MyDb.db')")
    
    def set_model(self,imodel,**kwargs):
        return self.setModel(imodel,**kwargs)
    
    def setModel(self,imodel,**kwargs):
        """Set The database"""
        self.__model=imodel
        return self.create_meta(self.__model,**kwargs)
    def getE(self):
        return self.e()
    def getEngine(self):
        return self.e()
    def get_e(self):
        return self.e()
    def get_engine(self):
        return self.e()
    def e(self):
        return self.__engine
    def getS(self,**kwargs):
        return self.__session
    def get_s(self,**kwargs):
        return self.__session
    def get_session(self,**kwargs):
        return self.__session
    def s(self):
        return self.__session
    def __s__(self,**kwargs):
        """Database Session"""
        if self.__db==None:
            self.setDb(self.__db,**kwargs)
        sm=sessionmaker(autoflush=self.autoflash,autocommit=self.autocommit,bind=self.__engine)
        self.__session=sm()
        return self.__session
    
    def ns(self):
        sm=sessionmaker(autoflush=self.autoflash,autocommit=self.autocommit,bind=self.__engine)
        return sm()
        
    """sqlalchemy override section start"""
    #"""
    def add(self,eobject):
        try:
            s=self.ns()
            s.add(eobject)
            s.flush()
            s.commit()
            return True
        except:return False
    
    def commit(self):
        try:
            s=self.ns()
            s.flush()
            s.commit()
            return True
        except:return False
    #"""    
    def query(self,**kwargs):
        if self.__model==None:
            raise NoModelDefined("No Database model is defined")
        return self.ns().query(self.__model)
    
    """sql alchemy override section end"""
    def get_tables(self):
        """Get All available tables"""
        rdata=[]
        try:
            eng=self.getEngine()
            c=eng.connect()
            cur=c.execute('SELECT name FROM sqlite_master WHERE type = "table"')
            data = cur.fetchall()
            for i in data:
                rdata.append(i[0])
        except Exception:
            return []
        return rdata
    
    def getTables(self):
        return self.get_tables()
    
    def create_meta(self,obj_db,**kwargs):
        if self.__engine==None:
            raise NoEngineDefined("Yo have not defined any engine.You must call setDb() to define engine.")
        if os.path.exists(self.__db):
            if os.path.getsize(self.__db)==0:
                obj_db.__bases__[0].metadata.create_all(self.e())
                return True
            else:
                tables=self.getTables()
                try:
                    tables.index(obj_db.__tablename__)
                    return True
                except Exception:
                    obj_db.__bases__[0].metadata.create_all(self.e())
                    return True
        else:
            obj_db.__bases__[0].metadata.create_all(self.e())
            return True
    
    def make_dirs(self,u_db):
        """make parent dirs"""
        dn=os.path.dirname(u_db)
        if dn!="":
            if not os.path.exists(dn):
                os.makedirs(dn)
################################  End of MyDbManager  #################################


############################## Start Of UserDbModel #################################
class UserDbModel(declarative_base()):
    """
    status
     0: Default( Just Added)
    -1: Trash
    
    wstatus
     0: Not Watched
     1: Watched
     2: Want To Watch
    info
      
    meta
    it is yours so u must maintain it in your own way
    """
    __tablename__="UserDb"
    uid = Column(Integer,primary_key=True)
    path = Column(Unicode)
    imdbid = Column(Unicode,default=u"None")
    cdate = Column(DateTime,default=datetime.datetime.utcnow)
    udate = Column(DateTime)
    status = Column(Integer,default=0)
    wstatus = Column(Integer,default=0)
    info = Column(Integer,default=0)
    meta = Column(Unicode,default=u"None")
    
    def __repr__(self):
        return "<UserDbModel (uid=%s,path=%s,imdbid=%s)>"%(self.uid,self.path,self.imdbid)
    
    def __init__(self,*kwards,**kwargs):
        if len(kwards)!=0:
            if len(kwards)==1:
                self.path,=kwards
                self.path=unicode(self.path)
        elif len(kwards)==2:
            self.path,self.imdbid=kwards
            self.path=unicode(self.path)
            self.imdbid=unicode(self.imdbid)
        elif len(kwards)==3:
            self.path,self.imdbid,self.status=kwards
            self.path=unicode(self.path)
            self.imdbid=unicode(self.imdbid)
            try:
                self.status=int(self.status)
            except:
                self.status=0
        elif len(kwards)==4:
            self.path,self.imdbid,self.status,self.wstatus=kwards
            self.path=unicode(self.path)
            self.imdbid=unicode(self.imdbid)
            try:
                self.status=int(self.status)
            except:
                self.status=0
            try:
                self.wstatus=int(self.wstatus)
            except:
                self.wstatus=0
        elif len(kwards)==5:
            self.path,self.imdbid,self.status,self.wstatus,self.meta=kwards
            self.path=unicode(self.path)
            self.imdbid=unicode(self.imdbid)
            try:
                self.status=int(self.status)
            except:
                self.status=0
            try:
                self.wstatus=int(self.wstatus)
            except:
                self.wstatus=0
            self.meta=unicode(self.meta)
        else:
            if kwargs.has_key("path"):self.path=unicode(kwargs["path"])
            if kwargs.has_key("imdbid"):self.imdbid=unicode(kwargs["imdbid"])
            else:self.imdbid=unicode("None")
            if kwargs.has_key("status"):
                try:self.status=int(kwargs["status"])
                except:self.status=0
            else:self.status=0
            if kwargs.has_key("wstatus"):
                try:self.wstatus=int(kwargs["wstatus"])
                except:self.wstatus=0
            else:self.wstatus=0
            if kwargs.has_key("meta"):self.meta=unicode(kwargs["meta"])
            else:self.meta=unicode("None") 
################## End Of UserDbModel ################   



##################### Start Of MovieDbModel ##########
class MovieDbModel(declarative_base()):
    __tablename__ = "MovieDb"
    imdbid = Column(Unicode,primary_key=True)
    imdbrating = Column(Float,default=0.0)
    year=Column(Integer,default=0)
    plot = Column(Unicode,default=u"None")
    rated = Column(Unicode,default=u"None")
    title = Column(Unicode,default=u"None")
    poster = Column(Unicode,default=u"None")
    writer = Column(Unicode,default=u"None")
    director = Column(Unicode,default=u"None")
    released = Column(Unicode,default=u"None")
    actors = Column(Unicode,default=u"None")
    genre = Column(Unicode,default=u"None")
    runtime = Column(Unicode,default=u"None")
    type = Column(Unicode,default=u"None")
    imdbvotes = Column(Unicode,default=u"None")
    meta = Column(Unicode,default=u"None")
    
    def has_key(self,key):
        if self.mdata.has_key(key):return True
        return False
    
    def get(self,key):return self.mdata[key]
    
    def __init__(self,*kwards,**kwargs):
        self.change(*kwards,**kwargs)
    
    def change(self,*kwards,**kwargs):
        """You Must Provide A dictionary"""
        self.mdata=None
        if len(kwards)==0:
            if kwargs.has_key("data"):
                self.mdata=kwargs["data"]
        elif len(kwards)==1:
            self.mdata,=kwards
        
        if self.mdata==None:
            raise ValueError,"You Must Provide A data Dictionary."
        else:
            if type(self.mdata)==dict:
                """Just Format The Keys to lower"""
                for i in self.mdata.keys():
                    self.mdata[i.lower()]=self.mdata[i]
                    #del self.mdata[i]
                ##### Now Assing It to corresponding Column #######
                if self.has_key("imdbid"):self.imdbid=self.get("imdbid")
                if self.has_key("imdbrating"):
                    try:self.imdbrating=float(self.get("imdbrating"))
                    except:self.imdbrating=0.0
                if self.has_key("year"):
                    try:self.year=int(self.get("year"))
                    except:self.year=0
                if self.has_key("plot"):self.plot=unicode(self.get("plot"))
                if self.plot==u"N/A":self.plot=u"None"
                if self.has_key("rated"):self.rated=unicode(self.get("rated"))
                if self.rated==u"N/A":self.rated=u"None"
                if self.has_key("title"):self.title=unicode(self.get("title"))
                if self.title==u"N/A":self.title=u"None"
                if self.has_key("poster"):self.poster=unicode(self.get("poster"))
                if self.poster==u"N/A":self.poster=u"None"
                if self.has_key("writer"):self.writer=unicode(self.get("writer"))
                if self.writer==u"N/A":self.writer=u"None"
                if self.has_key("director"):self.director=unicode(self.get("director"))
                if self.director==u"N/A":self.director=u"None"
                if self.has_key("released"):self.released=unicode(self.get("released"))
                if self.released==u"N/A":self.released=u"None"
                if self.has_key("actors"):self.actors=unicode(self.get("actors"))
                if self.actors==u"N/A":self.actors=u"None"
                if self.has_key("genre"):self.genre=unicode(self.get("genre"))
                if self.genre==u"N/A":self.genre=u"None"
                if self.has_key("runtime"):self.runtime=unicode(self.get("runtime"))
                if self.runtime==u"N/A":self.runtime=u"None"
                if self.has_key("type"):self.type=unicode(self.get("type"))
                if self.type==u"N/A":self.type=u"None"
                if self.has_key("imdbvotes"):self.imdbvotes=unicode(self.get("imdbvotes"))
                if self.imdbvotes==u"N/A":self.imdbvotes=u"None"
                if self.has_key("meta"):self.meta=unicode(self.get("meta"))
            else:raise ValueError,"Given Data is Unsupported.You Must Provide A data Dictionary."
################## End of MovieDbModel ####################################


########################### Start of TagDbModel ###########################
class TagDbModel(declarative_base()):
    __tablename__ = "TagDb"
    tid = Column(Integer,primary_key=True)
    tag = Column(Unicode)
    uids = Column(Unicode)
    def __init__(self,tag,uids):
        self.tag=unicode(tag)
        self.uids=unicode(uids)
############# End of TagDbModel ######################

################################# End Of Db Modeling ###############################





################################## Movie Fetcher Apis ##############################
######################################### IMDB info Featcher ###################################################
class OmdbApiException(Exception):
    def __init__(self,msg):self.msg = msg
    def __str__(self):return repr(self.msg)


class InvalidId(OmdbApiException):pass
class InvalidYear(OmdbApiException):pass
class InvalidInput(OmdbApiException):pass
class InvalidSearch(OmdbApiException):pass
class MovieNotFound(OmdbApiException):pass
class NetworkError(OmdbApiException):pass




class OmdbApi(object):
    """Open Movie DataBase Api"""
    def __init__(self):
        self.__base_url="http://www.omdbapi.com"
        #self.__i=None#Valid IMDB movie id
        #self.__t=None#Movie title
        #self.__y=None#Movie release year
        self.__r="JSON"#Movie return format,JSON or XML
        self.__plot="full"#Movie Plot full or short
    def setPlotFull(self):self.__plot="full"
    def setPlotShort(self):self.__plot="short"
        
    def urlencode_utf8(self,params):
        if hasattr(params, 'items'):
            params = params.items()
            return '&'.join((quote_plus(k.encode('utf8'), safe='/') + '=' + quote_plus(v.encode('utf8'), safe='/') for k, v in params))
        
    def encoder(self,dict_data):return self.urlencode_utf8(dict_data)
        
    def search(self,**kwargs):
            """Search Movie and get movie list by using this method"""
            get_url=None
            data=None
            y=None
            s=None
            if kwargs.has_key("s"):s=kwargs["s"]
            else:raise InvalidSearch("You have not provide any search string")
            if kwargs.has_key("y"):
                y=kwargs["y"]
                try:y=int(y)
                except Exception:raise InvalidYear("Check the y (year) parameter it must be a number")
                y=str(y)
            if y==None:get_url=self.__base_url+"/?"+self.encoder({"s":s,"r":self.__r,"plot":self.__plot})
            else:get_url=self.__base_url+"/?"+self.encoder({"y":y,"s":s,"r":self.__r,"plot":self.__plot})
            if get_url==None:raise InvalidInput("You have not provide s parameter (search string)")
            elif get_url!=None:
                try:
                    u = urllib2.urlopen(get_url)
                    data=json.load(u)
                    u.close()
                except Exception:return None
                if data.has_key("Error"):
                    #print data["Error"]
                    if data["Error"].lower()=="Movie Not Found!".lower():raise MovieNotFound("Movie Not Found")
                    else:raise OmdbApiException(data["Error"])
                if data!=None:
                    if data.has_key("Response"):del data["Response"]
                    if data.has_key("Search"):
                        ndata=[]
                        for mv in data["Search"]:
                            for ikey in mv.keys():
                                mv[ikey.lower()]=mv[ikey]
                            ndata.append(mv)
                        return ndata
            return None
        
    def get(self,**kwargs):
            """get Movie info dictionary using this method"""
            get_url=None
            data=None
            i=None
            y=None
            t=None
            if kwargs.has_key("i"):i=kwargs["i"]
            elif kwargs.has_key("t"):t=kwargs["t"]
            
            if kwargs.has_key("y"):
                y=kwargs["y"]
                try:
                    y=int(y)
                except Exception:
                    raise InvalidYear("Check the y (year) parameter it must be a number")
                y=str(y) 
                
            if i!=None:
                if not i.startswith("tt"):raise InvalidId("Invalid IMDB ID")
                get_url=self.__base_url+"/?"+self.encoder({"i":i,"r":self.__r,"plot":self.__plot})
            elif t!=None:
                if y==None:get_url=self.__base_url+"/?"+self.encoder({"t":t,"r":self.__r,"plot":self.__plot})
                else:get_url=self.__base_url+"/?"+self.encoder({"t":t,"y":y,"r":self.__r,"plot":self.__plot})
            if get_url==None:raise InvalidInput("You have not provide i (imdb id) or t (imdb title)")
            elif get_url!=None:
                try:
                    u = urllib2.urlopen(get_url)
                    data=json.load(u)
                    u.close()
                    #print data
                    #except Urlopen
                except Exception:
                    raise NetworkError("Error on network connection")
                    return None
                if data.has_key("Error"):
                    #print data["Error"]
                    if data["Error"].lower()=="Movie Not Found!".lower():raise MovieNotFound("Movie Not Found")
                    else:raise OmdbApiException(data["Error"])
            
            if data!=None:
                if data.has_key("Response"):del data["Response"]
                for i in data.keys():data[i.lower()]=data[i]
                return data
            return None

################################## End Of Movie Fetcher Apis ##################
















##################### Imovman DataBase #############
class IDb(object):
    """iMovMan Database Maintainer"""
    def __init__(self,*kwards,**kwargs):
        self.reset(*kwards,**kwargs)
    
    
    def __add_error(self,msg):
        if len(self.__error)>=100:
            del(self.__error[0])
        self.__error.append(msg)
    
    
    def get_last_error(self):
        if len(self.__error)!=0:
            n=len(self.__error)-1
            e=self.__error[n]
            del self.__error[n]
            return e
    
            
    def get_errors(self):return self.__error
    
    
    def reset(self,*kwards,**kwargs):
        self.movie_db_keys=["Title",
               "imdbRating",
               "Genre",
               "Year",
               "Runtime",
               "Released",
               "Actors",
               "Director",
               "Writer",
               "Rated",
               "imdbVotes",
               "imdbID",
               "Plot",
               "Poster",
               "Type"]
        
        
        self.movie_path=None #Movie Path
        self.udb=os.path.realpath(os.path.join(config.C_DATA_DIR,"db/user_db.idb"))
        self.mdb=os.path.realpath(os.path.join(config.C_DATA_DIR,"db/movie_db.idb"))
        self.tdb=os.path.realpath(os.path.join(config.C_DATA_DIR,"db/tag_db.idb"))
        self.__error=[]
        self.mfapi=None
        
        self.udb_m=None
        self.udb_s=None
        
        self.mdb_m=None
        self.mdb_s=None
        
        self.tdb_m=None
        self.tdb_s=None
        
        self.cover_format=config.C_COVER_FORMAT
        
        
        
        try:
            self.udb_m=MyDbManager(db=self.udb,model=UserDbModel)
            self.udb_s=self.udb_m.s()#session
        except Exception,e:print e
        
        try:
            self.mdb_m=MyDbManager(db=self.mdb,model=MovieDbModel)
            self.mdb_s=self.mdb_m.s()#session
        except Exception,e:print e
        
        try:
            self.tdb_m=MyDbManager(db=self.tdb,model=TagDbModel)
            self.tdb_s=self.tdb_m.s()#session
        except Exception,e:print e
        
        """Movie Fetcher Api Configuration"""
        if kwargs.has_key("mfapi"):
            if kwargs["mfapi"]==1 or kwargs["mfapi"]=="1":self.mfapi=OmdbApi()
        if self.mfapi==None:self.mfapi=OmdbApi()
    
    def reset_udb(self):
        try:
            self.udb_m=MyDbManager(db=self.udb,model=UserDbModel)
            self.udb_s=self.udb_m.s()#session
        except Exception,e:print e
    
    def new_udbs(self):
        try:
            udb_m=MyDbManager(db=self.udb,model=UserDbModel)
            udb_s=udb_m.s()#session
            return udb_s
        except:
            return None
        
    def reset_mdb(self):
        try:
            self.mdb_m=MyDbManager(db=self.mdb,model=MovieDbModel)
            self.mdb_s=self.mdb_m.s()#session
        except Exception,e:print e
    
    def reset_tdb(self):
        try:
            self.tdb_m=MyDbManager(db=self.tdb,model=TagDbModel)
            self.tdb_s=self.tdb_m.s()#session
        except Exception,e:print e
        
        
        
        
    def has_udb_path(self,mpath=None):
        if mpath==None:path=self.movie_path
        else:path=mpath
        path=unicode(path)
        if path!=None:
            try:
                s=self.udb_m.ns()
                inst=s.query(UserDbModel).filter(UserDbModel.path==path).filter(or_(UserDbModel.status==0,UserDbModel.status==1)).first()
                if inst==None:return False
                else:return True
            except:return False
        return None

    
    def get_udb_by_path(self,path):
        path=unicode(path)
        try:
            s=self.udb_m.ns()
            return s.query(UserDbModel).filter(UserDbModel.path==path).filter(or_(UserDbModel.status==0,UserDbModel.status==1)).first()
        except:return None
        return None
    
    
    def has_udb_imdbid(self,imdbid):
        imdbid=unicode(imdbid)
        try:
            s=self.udb_m.ns()
            inst=s.query(UserDbModel).filter(UserDbModel.imdbid==imdbid).filter(or_(UserDbModel.status==0,UserDbModel.status==1)).first()
            if inst==None:return False
            else:return True
        except:return False
        return None    
    
    def get_udb_by_imdbid(self,imdbid):
        imdbid=unicode(imdbid)
        try:
            s=self.udb_m.ns()
            return s.query(UserDbModel).filter(UserDbModel.imdbid==imdbid).filter(or_(UserDbModel.status==0,UserDbModel.status==1)).first()
        except:return None
        return None
    
    
    
    def has_mdb_imdbid(self,imdbid):
        imdbid=unicode(imdbid)
        try:
            s=self.mdb_m.ns()
            inst=s.query(MovieDbModel).filter(MovieDbModel.imdbid==imdbid).first()
            if inst==None:return False
            else:return True
        except:return False
        return None    
    
    def get_mdb_by_imdbid(self,imdbid):
        imdbid=unicode(imdbid)
        try:
            s=self.mdb_m.ns()
            return s.query(MovieDbModel).filter(MovieDbModel.imdbid==imdbid).first()
        except:return None
        return None
    
    
    def update_status(self,path,status):
        try:
            #-1 to delete
            #
            #
            s=self.new_udbs()
            if s!=None:
                s.query(UserDbModel).filter(UserDbModel.path==unicode(path)).update({'status': status})
                s.commit()
                return True
            else:
                print "Session is None..."
                return False
        except:
            error()
            return False    
    
    def update_wstatus(self,path,wstatus):
        try:
            #O not watched
            #1 watched
            #2 want to watch
            s=self.new_udbs()
            if s!=None:
                s.query(UserDbModel).filter(UserDbModel.path==unicode(path)).update({'wstatus': wstatus})
                s.commit()
                return True
            else:
                print "Session is None..."
                return False
        except:
            error()
            return False
    
    
    def add(self,mpath):
        #dir_name=os.path.dirname(mpath)
        #self.reset_mdb()
        #self.reset_tdb()
        #self.reset_udb()
        
        movie_name=os.path.basename(mpath)#name of the movie with extension
        
        movie_format=self.get_format(mpath)#movie file format
        
        movie_name=movie_name.replace("."+movie_format,"")#movie name without format
        
        data_path=mpath.replace(movie_format,"txt")#text info file path
        self.movie_path=unicode(mpath)#Movie Path
        #print self.movie_path
        #print self.has_udb_path()
        ### If the path donot exists in db######
        if not self.has_udb_path():
            udb_model=UserDbModel(self.movie_path)
            try:
                self.udb_s.add(udb_model)
                #self.udb_s.add(udb_model)
            except Exception,e:
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname,lineno,fn,text = frame
                    self.__add_error("[%s:%d] - %s --%s" % (fname+" "+whoami(),lineno,text,fn))
                    #print e
        else:
            udb_model=self.get_udb_by_path(self.movie_path)
        
        title,year=get_smart_name(movie_name)
        not_found=False#movie found or not
        fetch_error=False#movie fetch error
        
        ###If Local Txt DataFile Doesnot Exists####
        if not os.path.exists(data_path):
            data=None
            if title!=None and year!=None:
                try:data=self.mfapi.get(t=title,y=year)
                except MovieNotFound,e:
                    print e,self.movie_path
                    not_found=True
                except Exception,e:
                    print e,self.movie_path
                    fetch_error=True
            elif  title!=None and year==None:
                try:data=self.mfapi.get(t=title)
                except MovieNotFound,e:
                    print e,self.movie_path
                    not_found=True
                except Exception,e:
                    print e,self.movie_path
                    fetch_error=True
            
            if data==None:
                fetch_error=False
                not_found=False
                try:
                    links=False
                    #title=movie_name
                    print "In Google ",title
                    if title!=None:links = getgooglelinks(title,'http://www.imdb.com')
                    #else:links=getgooglelinks(movie_name,'http://www.imdb.com')
                    #print links," ++++ ",title
                    if links==False:
                        fetch_error=True
                        not_found=True
                    if links!=False:
                        imdbid=get_imdbid(links[0])
                        print imdbid
                        try:
                            data=self.mfapi.get(i=imdbid)
                            #print data
                        except Exception,e:
                            print e
                            fetch_error=True
                except Exception,e:
                    print e
                    not_found=True
            
            if not fetch_error and not not_found:
                if data!=None:
                    #print data
                    self.make_txt(data,data_path)
        if os.path.exists(data_path):
            data=self.form_dict(data_path)
            #print data
            
            ####Download Cover if not exists####
            has_cover=False
            for i in self.cover_format:
                if self.cover_exists(data_path.replace("txt",i)):
                    has_cover=True
                    break
            if not has_cover:
                if data.has_key("Poster"):
                    if data["Poster"]!="N/A":
                        cov_path=data_path.replace("txt","jpg")
                        self.getCover(data["Poster"],cov_path)
            ##### Cover Section Done #############
            
            #### If the data not in MovieDb Data base Add it######
            mdm=MovieDbModel(data)#Movie Database Model
            if not self.has_mdb_imdbid(mdm.imdbid):
                try:
                    self.mdb_s.add(mdm)
                except Exception,e:
                    self.__add_error(my_error(e))
                    #print e
            
            ##### Just Update The imdbid of the movie path of user database######
            #print mpath,mdm.imdbid==udb_model.imdbid,mdm.imdbid
            if mdm.imdbid!=udb_model.imdbid:
                udb_model.imdbid=mdm.imdbid
                try:
                    #print "Updating imdb id udb"
                    self.udb_s.add(udb_model)
                except Exception,e:
                    self.__add_error(my_error(e))
                    #print e
        else:
            #if data path not exists
            if not_found:udb_model.info=2            
            if fetch_error:udb_model.info=3
            
            #"""
            try:
                self.udb_s.add(udb_model)
            except Exception,e:
                self.__add_error(my_error(e))
            #"""
        
        try:
            #print "Updating imdb id udb"
            self.mdb_s.flush()
            self.mdb_s.commit()
            
            self.udb_s.flush()
            self.udb_s.commit()
            #self.udb_s.add(udb_model)
        except Exception,e:
            self.__add_error(my_error(e))
            #print e
    
    
    def map_object(self,obj,dict_data):
        return obj
    
    
    
    def update_mdb_by_imdbid(self,aimdbid,**kwargs):
        mdb=self.get_mdb_by_imdbid(aimdbid)
        if mdb==None:return False
        for i in kwargs.keys():
            exec("mdb.%s = %s" % ( i ,  repr( unicode(kwargs[i]) )   ) )
            
        try:
            self.mdb_s.add(mdb)
            self.mdb_s.flush()
            self.mdb_s.commit()
            return True
        except Exception,e:
            self.__add_error(my_error(e))    
            return False
    
    
    
    
    def update_udb_by_path(self,path,**kwargs):
        ins=self.get_udb_by_path(path)
        if ins==None:return False
        for i in kwargs.keys():
            exec("ins.%s = %s" % ( i ,  repr( unicode(kwargs[i]) )   ) )       
        try:
            self.udb_s.add(ins)
            self.udb_s.flush()
            self.udb_s.commit()
            return True
        except Exception,e:
            self.__add_error(my_error(e) )    
            return False
        
    
    
    def get_movie_by_imdbid(self,imdbid,**kwargs):
        imdbid=unicode(imdbid)
        data={}
        
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.ns().query(UserDbModel).filter( or_( UserDbModel.status==0,UserDbModel.status==1) ).filter(UserDbModel.imdbid==imdbid)
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                
                cov_path="None"
                for i in self.cover_format:
                    cov_path=udb.path.replace(self.get_format(udb.path),i)
                    if os.path.exists(cov_path):break
                movie["local_cover"]=cov_path
                
                
                if udb.imdbid!=u"None":
                    mdb=self.get_mdb_by_imdbid(udb.imdbid)
                    if mdb!=None:
                        for i in self.movie_db_keys:
                            i=i.lower()
                            exec('movie["%s"] = mdb.%s' % (i ,i) ) 
                data=movie
                
        except Exception,e:self.__add_error(my_error(e))
        if rtype=="json":return json.dumps(data)
        else:return data        
        
    def get_all_movies(self,**kwargs):
        data=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.ns().query(UserDbModel).filter( or_( UserDbModel.status==0,UserDbModel.status==1) ).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                
                cov_path="None"
                for i in self.cover_format:
                    cov_path=udb.path.replace(self.get_format(udb.path),i)
                    if os.path.exists(cov_path):break
                movie["local_cover"]=cov_path
                
                
                if udb.imdbid!=u"None":
                    mdb=self.get_mdb_by_imdbid(udb.imdbid)
                    if mdb!=None:
                        for i in self.movie_db_keys:
                            i=i.lower()
                            exec('movie["%s"] = mdb.%s' % (i ,i) ) 
                data.append(movie)
                
        except Exception,e:self.__add_error(my_error(e))
        if rtype=="json":return json.dumps(data)
        else:return data
        
    def sort_by_rating(self,**kwargs):
        data=[]
        ldata=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.query().filter( UserDbModel.status!=-1 ).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                
                cov_path="None"
                for i in self.cover_format:
                    cov_path=udb.path.replace(self.get_format(udb.path),i)
                    if os.path.exists(cov_path):break
                movie["local_cover"]=cov_path
                
                
                if udb.imdbid!=u"None":
                    mdb=self.get_mdb_by_imdbid(udb.imdbid)
                    if mdb!=None:
                        for i in self.movie_db_keys:
                            i=i.lower()
                            exec('movie["%s"] = mdb.%s' % (i ,i) )
                        data.append(movie)
                else:
                    movie["title"]=os.path.basename(udb.path)
                    movie["year"]="0"
                    movie["imdbrating"]="0.0"
                    ldata.append(movie) 
                
            ###########################
            data.sort(key=operator.itemgetter('imdbrating'))
            data.reverse()
            data=data+ldata
                
        except Exception,e:self.__add_error(my_error(e))
        
        if rtype=="json":return json.dumps(data)
        else:return data
    
    def sort_by_year(self,**kwargs):
        data=[]
        ldata=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.query().filter( UserDbModel.status!=-1 ).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                
                cov_path="None"
                for i in self.cover_format:
                    cov_path=udb.path.replace(self.get_format(udb.path),i)
                    if os.path.exists(cov_path):break
                movie["local_cover"]=cov_path
                
                
                if udb.imdbid!=u"None":
                    mdb=self.get_mdb_by_imdbid(udb.imdbid)
                    if mdb!=None:
                        for i in self.movie_db_keys:
                            i=i.lower()
                            exec('movie["%s"] = mdb.%s' % (i ,i) )
                        data.append(movie)
                else:
                    movie["title"]=os.path.basename(udb.path)
                    movie["year"]="0"
                    movie["imdbrating"]="0.0"
                    ldata.append(movie) 
                
            ###########################
            data.sort(key=operator.itemgetter('year'))
            data.reverse()
            data=data+ldata
                
        except Exception,e:self.__add_error(my_error(e))
        
        if rtype=="json":return json.dumps(data)
        else:return data    
    
    def get_not_found_movies(self,**kwargs):
        data=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.query().filter( UserDbModel.info==2 ).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                movie["local_cover"]="None"
                data.append(movie)
        except Exception,e:self.__add_error(my_error(e))
        if rtype=="json":return json.dumps(data)
        else:return data
        
    
    
    def get_fetch_error_movies(self,**kwargs):
        data=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.query().filter( UserDbModel.info==3 ).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                movie["local_cover"]="None"
                data.append(movie)    
        except Exception,e:self.__add_error(my_error(e))
        if rtype=="json":return json.dumps(data)
        else:return data    
    
    
    
    def get_trashed_movies(self,**kwargs):
        data=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.query().filter( UserDbModel.status==-1 ).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                movie["local_cover"]="None"
                
                
                if udb.imdbid!=u"None":
                    mdb=self.get_mdb_by_imdbid(udb.imdbid)
                    if mdb!=None:
                        for i in self.movie_db_keys:
                            i=i.lower()
                            exec('movie["%s"] = mdb.%s' % (i ,i) ) 
                data.append(movie)
                
        except Exception,e:self.__add_error(my_error(e))
        
        if rtype=="json":return json.dumps(data)
        else:return data
        
    
    
    def get_tags(self,**kwargs):
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        
        if kwargs.has_key("section"):section=kwargs["section"].lower()
        else:section="all"
        
        
        if kwargs.has_key("tag"):
            tag=kwargs["tag"].lower()
            ptag=tag
            tag=unicode("%"+tag+"%")
        else:
            tag="all"
            ptag=None
                           
        
        
        
        data=[]
        if section=="title" or section=="all":
            try:
                if tag=="all":instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.title)
                else:instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.title).filter(MovieDbModel.title.like(tag))
                for ins in instances:
                    if self.has_udb_imdbid(ins.imdbid):
                        temp={}
                        temp["name"]=ins.title
                        temp["dtype"]="title"
                        temp["imdbid"]=ins.imdbid
                        data.append(temp)
            except Exception,e:self.__add_error(my_error(e))
                    
        """Writer Section"""
        if section=="writer" or section=="all":
            try:
                if tag=="all":instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.writer)
                else:instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.writer).filter(MovieDbModel.writer.like(tag))
                for ins in instances:
                    if self.has_udb_imdbid(ins.imdbid):
                        splitted=ins.writer.split(",")
                        for s in splitted:
                            s=s.strip().lower()
                            if ptag!=None:
                                if s.find(ptag.lower())!=-1:
                                    temp={}
                                    temp["name"]=s.capitalize()
                                    temp["dtype"]="writer"
                                    if temp not in data:
                                        data.append(temp)
                            else:
                                temp={}
                                temp["name"]=s.capitalize()
                                temp["dtype"]="writer"
                                if temp not in data:
                                    data.append(temp)
            except Exception,e:self.__add_error(my_error(e))
        
        """Director Section"""
        if section=="director" or section=="all":
            try:
                if tag=="all":
                    instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.director)
                else:
                    instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.director).filter(MovieDbModel.director.like(tag))
                for ins in instances:
                    if self.has_udb_imdbid(ins.imdbid):
                        splitted=ins.director.split(",")
                        for s in splitted:
                            s=s.strip().lower()
                            if ptag!=None:
                                if s.find(ptag.lower())!=-1:
                                    temp={}
                                    temp["name"]=s.capitalize()
                                    temp["dtype"]="director"
                                    if temp not in data:data.append(temp)
                            else:
                                temp={}
                                temp["name"]=s.capitalize()
                                temp["dtype"]="director"
                                if temp not in data:data.append(temp)
            except Exception,e:self.__add_error(my_error(e))        
        
        """Actor Section"""
        if section=="actor" or section=="all":
            try:
                if tag=="all":instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.actors)
                else:instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.actors).filter(MovieDbModel.actors.like(tag))
                for ins in instances:
                    if self.has_udb_imdbid(ins.imdbid):
                        splitted=ins.actors.split(",")
                        for s in splitted:
                            s=s.strip().lower()
                            if ptag!=None:
                                if s.find(ptag.lower())!=-1:
                                    temp={}
                                    temp["name"]=s.capitalize()
                                    temp["dtype"]="actor"
                                    if temp not in data:data.append(temp)
                            else:
                                temp={}
                                temp["name"]=s.capitalize()
                                temp["dtype"]="actor"
                                if temp not in data:data.append(temp)
            except Exception,e:self.__add_error(my_error(e))        
        
        """Genre Section"""
        if section=="genre" or section=="all":
            try:
                if tag=="all":instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.genre)
                else:instances=self.mdb_m.ns().query(MovieDbModel.imdbid,MovieDbModel.genre).filter(MovieDbModel.genre.like(tag))
                for ins in instances:
                    if self.has_udb_imdbid(ins.imdbid):
                        splitted=ins.genre.split(",")
                        for s in splitted:
                            s=s.strip().lower()
                            if ptag!=None:
                                if s.find(ptag.lower())!=-1:
                                    temp={}
                                    temp["name"]=s.capitalize()
                                    temp["dtype"]="genre"
                                    if temp not in data:data.append(temp)
                            else:
                                temp={}
                                temp["name"]=s.capitalize()
                                temp["dtype"]="genre"
                                if temp not in data:data.append(temp)
            except Exception,e:self.__add_error(my_error(e))        
        
        data=self.make_unique_list(data)
        if rtype=="json":return json.dumps(data)
        else:return data   
    
    
    
    def get_genres(self,**kwargs):
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        rlist=[]
        
        try:
            s=self.mdb_m.ns()
            mdbs=s.query(MovieDbModel.imdbid,MovieDbModel.genre).all()
            for mdb in mdbs:
                if self.has_udb_imdbid(mdb.imdbid):
                    splitted_gen=mdb.genre.split(",")
                    for s in splitted_gen:
                        s=s.strip().lower().capitalize()
                        try:rlist.index(s)
                        except:rlist.append(s)
        except Exception,e:self.__add_error(my_error(e))
        #rlist.sort()
        if rtype=="json":return json.dumps(rlist)
        elif rtype=="python":return rlist
        return rlist
    
    
    def get_stat(self,**kwargs):
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        data={}
        t=len(self.get_all_movies(rtype="python"))
        data["get_all_movies"]=t
        data["total_movies"]=t
        data["get_not_found_movies"]=len(self.get_not_found_movies(rtype="python"))
        data["get_fetch_error_movies"]=len(self.get_fetch_error_movies(rtype="python"))
        #print data
        
        if rtype=="json":return json.dumps(data)
        else:return data
        
    def load_movies_all(self,**kwargs):
        data=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.query().filter( UserDbModel.status!=-1 ).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                
                cov_path="None"
                for i in self.cover_format:
                    cov_path=udb.path.replace(self.get_format(udb.path),i)
                    if os.path.exists(cov_path):break
                movie["local_cover"]=cov_path
                
                
                if udb.imdbid!=u"None":
                    mdb=self.get_mdb_by_imdbid(udb.imdbid)
                    if mdb!=None:
                        for i in self.movie_db_keys:
                            i=i.lower()
                            exec('movie["%s"] = mdb.%s' % (i ,i) )
                else:
                    movie["title"]=os.path.basename(udb.path)
                    #movie["year"]=""
                    movie["imdbrating"]="0.0" 
                data.append(movie)
                
        except Exception,e:self.__add_error(my_error(e))
        
        if rtype=="json":return json.dumps(data)
        else:return data    
    
    def load_notwatched_movies(self,**kwargs):
        data=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.query().filter( UserDbModel.status!=-1 ).filter(UserDbModel.wstatus==0).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                
                cov_path="None"
                for i in self.cover_format:
                    cov_path=udb.path.replace(self.get_format(udb.path),i)
                    if os.path.exists(cov_path):break
                movie["local_cover"]=cov_path
                
                
                if udb.imdbid!=u"None":
                    mdb=self.get_mdb_by_imdbid(udb.imdbid)
                    if mdb!=None:
                        for i in self.movie_db_keys:
                            i=i.lower()
                            exec('movie["%s"] = mdb.%s' % (i ,i) )
                else:
                    movie["title"]=os.path.basename(udb.path)
                    #movie["year"]=""
                    movie["imdbrating"]="0.0"  
                data.append(movie)
                
        except Exception,e:self.__add_error(my_error(e))
        
        if rtype=="json":return json.dumps(data)
        else:return data
                
    def load_watched_movies(self,**kwargs):
        data=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.query().filter( UserDbModel.status!=-1 ).filter(UserDbModel.wstatus==1).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                
                cov_path="None"
                for i in self.cover_format:
                    cov_path=udb.path.replace(self.get_format(udb.path),i)
                    if os.path.exists(cov_path):break
                movie["local_cover"]=cov_path
                
                
                if udb.imdbid!=u"None":
                    mdb=self.get_mdb_by_imdbid(udb.imdbid)
                    if mdb!=None:
                        for i in self.movie_db_keys:
                            i=i.lower()
                            exec('movie["%s"] = mdb.%s' % (i ,i) )
                else:
                    movie["title"]=os.path.basename(udb.path)
                    #movie["year"]=""
                    movie["imdbrating"]="0" 
                data.append(movie)
                
        except Exception,e:self.__add_error(my_error(e))
        
        if rtype=="json":return json.dumps(data)
        else:return data
        
    def load_wanttowatch_movies(self,**kwargs):
        data=[]
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        try:
            udbs=self.udb_m.query().filter( UserDbModel.status!=-1 ).filter(UserDbModel.wstatus==2).all()
            for udb in udbs:
                movie={}#contain The Movie
                movie["id"]=udb.uid
                movie["uid"]=udb.uid
                movie["path"]=udb.path
                movie["imdbid"]=udb.imdbid
                movie["cdate"]=str(udb.cdate)
                movie["udate"]=str(udb.udate)
                movie["status"]=udb.status
                movie["wstatus"]=udb.wstatus
                movie["info"]=udb.info
                movie["meta"]=udb.meta
                
                cov_path="None"
                for i in self.cover_format:
                    cov_path=udb.path.replace(self.get_format(udb.path),i)
                    if os.path.exists(cov_path):break
                movie["local_cover"]=cov_path
                
                
                if udb.imdbid!=u"None":
                    mdb=self.get_mdb_by_imdbid(udb.imdbid)
                    if mdb!=None:
                        for i in self.movie_db_keys:
                            i=i.lower()
                            exec('movie["%s"] = mdb.%s' % (i ,i) )
                else:
                    movie["title"]=os.path.basename(udb.path)
                    #movie["year"]=""
                    movie["imdbrating"]="0" 
                data.append(movie)
                
        except Exception,e:self.__add_error(my_error(e))
        
        if rtype=="json":return json.dumps(data)
        else:return data
        
    def search_movies(self,**kwargs):
        if kwargs.has_key("rtype"):rtype=kwargs["rtype"].lower()
        else:rtype="json"
        data=[]
        if kwargs.has_key("tag"):
            tag=kwargs["tag"].lower()
            tag=unicode("%"+tag+"%")
        else:
            tag=None
            
        try:
            s=self.mdb_m.ns()
            #print s
            if tag!=None:instances=s.query(MovieDbModel).filter( or_( MovieDbModel.plot.like(tag),MovieDbModel.title.like(tag) , MovieDbModel.genre.like(tag), MovieDbModel.writer.like(tag), MovieDbModel.director.like(tag), MovieDbModel.actors.like(tag) )  ).all()
            else:instances=s.query(MovieDbModel).all()
                 
            for mdb in instances:
                if self.has_udb_imdbid(mdb.imdbid):
                    movie={}
                    for i in self.movie_db_keys:
                        i=i.lower()
                        exec('movie["%s"] = mdb.%s' % (i ,i) )
                    udb=self.get_udb_by_imdbid(mdb.imdbid)
                    if udb!=None:
                        movie["id"]=udb.uid
                        movie["uid"]=udb.uid
                        movie["path"]=udb.path
                        movie["imdbid"]=udb.imdbid
                        movie["cdate"]=str(udb.cdate)
                        movie["udate"]=str(udb.udate)
                        movie["status"]=udb.status
                        movie["wstatus"]=udb.wstatus
                        movie["info"]=udb.info
                        movie["meta"]=udb.meta
                        cov_path="None"
                        for i in self.cover_format:
                            cov_path=udb.path.replace(self.get_format(udb.path),i)
                            if os.path.exists(cov_path):break
                        movie["local_cover"]=cov_path
                    data.append(movie)
        except:
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                self.__add_error("[%s:%d] - %s --%s" % (fname+" "+whoami(),lineno,text,fn))
        
        
        if rtype=="json":return json.dumps(data)
        elif rtype=="python":return data
        return data
        
    

    
    def trash_manager(self):
        inss=self.udb_m.query().all()
        for ins in inss:
            if not os.path.exists(ins.path):
                if ins.status!=-1:self.update_status(ins.path,-1)
            else:
                if ins.status==-1:self.update_status(ins.path,-1)  
        
    
    
    
    
    
    
    
    
    
    
    """Some Helper Function"""
    def make_unique_list(self,rlist):
        name_list=[]
        new_return_list=[]
        for i in rlist:
            if i["name"] not in name_list:
                name_list.append(i["name"])
                new_return_list.append(i)
        return new_return_list
    
    
    
    def cover_exists(self,path):
        if os.path.exists(path):return True
        else:return False
    
    
    def get_format(self,name):return name.split(".")[-1]
    
    
    def form_dict(self,path):
        """This Will Form the dictionary From the text data"""
        dkeys=["Title",
               "imdbRating",
               "Genre",
               "Year",
               "Runtime",
               "Released",
               "Actors",
               "Director",
               "Writer",
               "Rated",
               "imdbVotes",
               "imdbID",
               "Plot",
               "Poster",
               "Type"]
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
        dkeys=[u"Title",
               u"imdbRating",
               u"Genre",
               u"Year",
               u"Runtime",
               u"Released",
               u"Actors",
               u"Director",
               u"Writer",
               u"Rated",
               u"imdbVotes",
               u"imdbID",
               u"Plot",
               u"Poster",
               u"Type"]
        if data:
            try:
                f=codecs.open(save_as, "w+", "utf-8")
                for i in dkeys:
                    if data.has_key(i):
                        f.write(i+": "+ data[i]+"\n")
                f.write("\n")
                f.write(u"SoftwareName: "+unicode(APP_NAME)+u"\n")
                f.write(u"SoftwareVersion: "+unicode(APP_VERSION)+u"\n")
                f.write(u"SoftwareDeveloper: "+unicode(APP_DEVELOPER)+u"\n")
                f.write(u"SoftwareHomepage: "+unicode(APP_WEB)+u"\n")
                f.close()
                return True
            except Exception,e:print e
        return False
    
    
    
    def get_smart_name(self,name):
        name=name.replace("1080p","").replace("720p","").replace("."," ").strip()
        pattern1=r'^(.*) \(([1-2][0-9][0-9][0-9])\)'
        pattern2=r'^(.*) ([1-2][0-9][0-9][0-9])'
        pattern3=r'^(.*)\.([1-2][0-9][0-9][0-9])'
        title=None
        year=None
        try:
            matchObj = re.match(pattern1,name, re.M|re.I)
            if matchObj:
                title=matchObj.group(1)
                year=matchObj.group(2)
            else:
                matchObj = re.match(pattern2,name, re.M|re.I)
                if matchObj:
                    title=matchObj.group(1)
                    year=matchObj.group(2)
                else:
                    matchObj = re.match(pattern3,name, re.M|re.I)
                    if matchObj:
                        title=matchObj.group(1)
                        year=matchObj.group(2)
                    else:
                        title=name
                if title!=None:title=title.replace("."," ").strip()
                return title,year
        except Exception,e:
            print e
            return title,year
        return title,year
    
    
    
    def getCover(self,url,save_as):
        """Get The Movie Cover"""
        f = urllib2.urlopen(url)
        with open(save_as,'wb') as output:
            while True:
                buf = f.read(65536)
                if not buf:break
                output.write(buf)
    
                
    def __set_error(self,frame):
        fname,lineno,fn,text = frame
        self.__add_error("[%s:%d] - %s --%s" % (fname+" "+whoami(),lineno,text,fn))



################# End of IDb ##############################################








######## Configuraion DataBase ###########################################
class ConfigDb(declarative_base()):
    __tablename__="ConfigDb"
    id = Column(Integer,primary_key=True)
    key = Column(Unicode)
    value = Column(Unicode)
    #itype = Column(Unicode)
    
    def __init__(self,**kwargs):
        self.id=None
        self.key=None
        self.value=None
        if kwargs.has_key("key"):self.key=unicode(kwargs["key"])
        if kwargs.has_key("value"):
            #self.itype=unicode(type(kwargs["value"]))
            self.value=unicode(kwargs["value"])
        
        try:self.cdb_m=MyDbManager(db=os.path.realpath(os.path.join(config.C_DATA_DIR,"db/config_db.idb")),model=ConfigDb)
        except:error()
        self.s=self.cdb_m.s()
        if self.key!=None and self.value==None:self.get(self.key)
        
        #self.itype=unicode(type(self.value))
        self.old_value=self.value
        self.old_key=self.key
    
    
    def get(self,key):
        try:
            ins=self.s.query(self.__class__).filter(self.__class__.key==unicode(key)).first()
            if ins!=None:
                self.id=ins.id
                self.key=ins.key
                self.value=ins.value
                #ins.value=ast.literal_eval(ins.value)
                #self.itype=ins.itype
                return ins
            else:
                error()
                return None
        except:
            return None
    
    
    def add(self,key,value):
        ikey=unicode(key)
        ins=self
        if self.has_key(ikey):
            
            #itype=unicode(type(value))
            value=unicode(value)
            
            ins=self.get(ikey)
            ins.value=value
            #ins.itype=itype
            self.old_value=ins.value
        else:
            ins=ConfigDb(key=key,value=value)
            #ins.key=ikey
            #ins.value=value
            #ins.itype=itype
            
        try:
            self.s.add(ins)
            self.s.flush()
            self.s.commit()
            return True
        except:
            error()
            return False
        return None
    
    def all(self):
        data={}
        try:
            inss=self.cdb_m.query().all()
            for ins in inss:
                data[ins.key]=ins.value
        except:
            error()
            return data
        return data
            
    def save(self):
        if self.value!=None and self.key!=None:
            try:
                self.add(self.key, self.value)
                self.get(self.key)
                return True
            except:
                error()
                return False
        return False
    
                        
    def has_key(self,key):
        try:
            ins=self.cdb_m.query().filter(ConfigDb.key==unicode(key)).first()
            if ins!=None:return True
            else:return False
        except Exception,e:
            print e
            error()
            return False
        
    def set_default(self):
        self.add("active_theme","'%s'"%config.C_DEFAULT_THEME)
        self.add("movie_format",config.C_MOVIE_FORMAT)
        self.add("theme_path","'%s'"%(config.C_THEME_PATH))
        self.add("drives", utility.get_drives())
        self.add("auto_crawl", False)
        self.add("setup",True)
        
        if not self.has_key("start_count"):
            self.add("start_count",0)
    
    def count(self):
        ins=self.get("start_count")
        if ins!=None:
            ins.value=int(ins.value)+1
            self.add("start_count", ins.value)
            return ins.value
        else:
            self.add("start_count",1)
            return 1
    
            
    def __repr__(self):
        return "<ConfigDb %s>"%(self.id)    
###################################################            
CDb=ConfigDb
######################End Of Config Db#############







if __name__=="__main__":
    idb=IDb()
    print idb.get_all_movies(tag="action")
    print idb.get_genres()
    print ast.literal_eval("None")
    #idb.add("F:\\MoviesWorld\\Satil\\Dave (1993)\\Dave (1993).mp4")
    #idb.trash_manager()
    #print sys.getsizeof(idb)
    #print idb.get_all_movies(rtype="python")
    #print idb.get_genres()
    #print idb.get_last_error()
    #print idb.get_trashed_movies()
    #print idb.get_tags()
    #print idb.search_movies(tag="kawser")
    #print idb.get_last_error()
    #print idb.get_stat()
    #import random
    #cdb=CDb()
    #cdb.add("k","'Smile2'")
    #my=ast.literal_eval(cdb.value)
    #print cdb.all()
    #cdb.set_default()
    #print cdb.count()

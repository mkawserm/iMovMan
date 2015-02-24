'''
Created on Jul 17, 2013

@author: KaWsEr
'''


import os
import ast
import sys
import string
import config
import threading
import traceback
#from PySide.QtCore import QObject,Signal

## ##
import util


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

######## Used By Db Models ###############
import datetime
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,Float,Unicode,DateTime,Binary

##


####################################################
def error():
    """TraceBack Error"""
    for frame in traceback.extract_tb(sys.exc_info()[2]):
        fname,lineno,fn,text = frame
        estr="[%s:%d] - Error:%s" % ("function ("+fn+") :: "+fname,lineno,text)
        #print estr
        return estr
##########################################
class MyDbManagerException(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)
##
  
class NoDataBaseDefined(MyDbManagerException):pass
class NoModelDefined(MyDbManagerException):pass
class NoEngineDefined(MyDbManagerException):pass
class NoSessionDefined(MyDbManagerException):pass
class UnknownError(MyDbManagerException):pass
##





######################################################################################
class MyDbManager(object):
    """MyDbManager is a sqllite database helper class for Sqlalchemy"""
    def __init__(self,**kwargs):
        self.semafor = threading.BoundedSemaphore(1)
        self.lock=threading.Lock()
        
        self.__db=None
        self.echo=False
        self.autoflash=False
        self.autocommit=False
        self.__engine=None
        self.__model=None
        self.__session=None
        self.__type="sqlite:///"
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
            self.__engine=create_engine(self.__type+self.__db, echo=self.echo)
            if self.__session==None:
                self.__s__()
        elif self.__db!=None:
            self.make_dirs(self.__db)
            self.__engine=create_engine(self.__type+self.__db, echo=self.echo)
            if self.__session==None:
                self.__s__()
        elif self.__db==None:
            raise NoDataBaseDefined("You have not provided any Database. example: object.s(db='MyDb.db')")
    
    def set_model(self,imodel,**kwargs):
        return self.setModel(imodel,**kwargs)
    
    def setModel(self,imodel,**kwargs):
        """Set The database"""
        self.__model=imodel
        
        self.lock.acquire()
        r=self.create_meta(self.__model,**kwargs)
        self.lock.release()
        
        return r
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
    def vaccum(self):self.e().execute("VACUUM")
        
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
        
        #self.semafor.acquire()
        if self.__engine==None:
            raise NoEngineDefined("Yo have not defined any engine.You must call setDb() to define engine.")
        if os.path.exists(self.__db):
            if os.path.getsize(self.__db)==0:
                obj_db.__bases__[0].metadata.create_all(self.e())
                #self.semafor.release()
                return True
            else:
                tables=self.getTables()
                try:
                    tables.index(obj_db.__tablename__)
                    #self.semafor.release()
                    return True
                except Exception:
                    obj_db.__bases__[0].metadata.create_all(self.e())
                    #self.semafor.release()
                    return True
        else:
            obj_db.__bases__[0].metadata.create_all(self.e())
            #self.semafor.release()
            return True
    
    def make_dirs(self,u_db):
        """make parent dirs"""
        dn=os.path.dirname(u_db)
        if dn!="":
            if not os.path.exists(dn):
                os.makedirs(dn)
################################  End of MyDbManager #################################

### Session Object Used By Databases Model ###########################################
class SOB(object):
    def __init__(self,db):
        self.db=db
        self.dm=MyDbManager(db=self.db)
    def set_model(self,model):self.dm.set_model(model)
    def vaccum(self):self.dm.vaccum()
    def s(self):return self.dm.s()
    def e(self):return self.dm.e()
    def ns(self):return self.s()
    def __repr__(self):return "<SOB id='%s'>"%str(id(self))
######################################################################################





## Options info of movies  ##
class OptionModel(declarative_base()):
    __tablename__="OptionDb"
    option_id=Column(Integer,primary_key=True)
    option_name=Column(Unicode)
    option_value=Column(Unicode)
    def __init__(self,*kwards,**kwargs):
        if len(kwards)==2:
            self.option_name=unicode(kwards[0])
            self.option_value=unicode(kwards[1])
    def __repr__(self):return "<OptionModel (option_id='%s') (option_name='%s')>"%(self.option_id,self.option_name)
## ----------------------------------------------------------- ##



class Option(object):
    def __init__(self,*kwards,**kwargs):
        self.__d=False
        self.__sob=None
        self.option_id=None
        self.option_name=None
        self.option_value=None
        if len(kwards)==0:
            self.__sob=SOB(config.DB_OPTION)
            self.__sob.set_model(OptionModel)
            
        if len(kwards)==1:
            self.__sob=kwards[0]
            if type(self.__sob)==SOB:
                self.__sob.set_model(OptionModel)
            elif type(self.__sob)==str:
                self.__sob=SOB(self.__sob)
                self.__sob.set_model(OptionModel)
    
    
    def add(self,name,value):
        s=self.s()
        self.option_id=None
        self.option_name=unicode(name)
        self.option_value=unicode(value)
        ins=s.query(OptionModel).filter(OptionModel.option_name==self.option_name).first()
        #print ins
        if ins==None:
            try:
                ins=OptionModel(self.option_name,self.option_value)
                s.add(ins)
                s.flush()
                s.commit()
                self.option_id=ins.option_id
                self.option_name=ins.option_name
                self.option_value=ins.option_value
                return True
            except Exception,e:
                self.derror(e)
                return False                
        return False


    def replace(self,name,value):
        s=self.s()
        self.option_name=unicode(name)
        self.option_value=unicode(value)
        ins=s.query(OptionModel).filter(OptionModel.option_name==self.option_name).first()
        #print ins
        if ins!=None:ins.option_value=self.option_value
        else:ins=OptionModel(self.option_name,self.option_value)
        #print ins                  
        try:
            s.add(ins)
            s.flush()
            s.commit()
            self.option_id=ins.option_id
            self.option_name=ins.option_name
            self.option_value=ins.option_value
            return ins
        except Exception,e:self.derror(e)
        return None

    def delete(self,**kwargs):
        s=self.s()
        dm=None
        try:
            if kwargs.has_key("option_id"):dm=s.query(OptionModel).filter(OptionModel.option_id==kwargs["option_id"]).one()
            elif kwargs.has_key("option_name"):dm=s.query(OptionModel).filter(OptionModel.option_name==unicode(kwargs["option_name"])).one()
            if dm!=None:
                s.delete(dm)
                s.commit()
                return True
        except Exception,e:self.derror(e)
        return False
    
    def update(self,**kwargs):
        s=self.s()
        if not kwargs.has_key("data"):return False
        else:
            for key in kwargs["data"].keys():
                kwargs["data"][key]=unicode(kwargs["data"][key])
        if kwargs["data"].has_key("option_id"):
            self.option_id=kwargs["data"]["option_id"]
            del kwargs["data"]["option_id"]
            if not self.has_option_id(self.option_id):
                self.reset()
                return False
            s.query(OptionModel).filter(OptionModel.option_id==self.option_id).update(kwargs["data"])
        elif kwargs["data"].has_key("option_name"):
            self.option_name=kwargs["data"]["option_name"]
            self.option_name=unicode(self.option_name)
            if not self.has_option(self.option_name):
                self.reset()
                return False
            del kwargs["data"]["option_name"]
            s.query(OptionModel).filter(OptionModel.option_name==self.option_name).update(kwargs["data"])
        else:return False
        try:
            s.commit()
            s.flush()
            return True
        except:pass
        return False
       
    
    def vaccum(self):self.__sob.e().execute("VACUUM")
        
        
    def __sub_get_option_name(self,option_name):
        try:
            r=self.s().query(OptionModel).filter(OptionModel.option_name==option_name ).first()
            temp={}
            if r!=None:
                temp["option_id"]=r.option_id
                temp["option_name"]=r.option_name
                temp["option_value"]=r.option_value
            return temp
        except Exception,e:
            #print e
            self.derror(e)
            return None
        
    def __sub_get_option_id(self,option_id):
        try:
            r=self.s().query(OptionModel).filter(OptionModel.option_id==option_id ).first()
            if r!=None:
                self.option_id=r.option_id
                self.option_name=r.option_name
                self.option_value=r.option_value
                temp={}
                temp["option_id"]=r.option_id
                temp["option_name"]=r.option_name
                temp["option_value"]=r.option_value
                return temp
            return {}
        except Exception,e:
            self.derror(e)
            return None
        
        
    def __sub_get_all(self):
        rlist=[]
        try:
            r=self.s().query(OptionModel).all()
            for i in r:
                temp={}
                temp["option_id"]=i.option_id
                temp["option_name"]=i.option_name
                temp["option_value"]=i.option_value
                rlist.append(temp)
                
            return rlist
        except Exception,e:
            self.derror(e)
            return None
        
        
        
    def get(self,*kwards,**kwargs):
        if kwargs.has_key("option_name"):
            option_name=kwargs["option_name"]
            try:option_name=unicode(option_name)
            except:return None
            return self.__sub_get_option_name(option_name)
        elif kwargs.has_key("option_id"):
            option_id=kwargs["option_id"]
            try:option_id=int(option_id)
            except:return None
            return self.__sub_get_option_id(option_id)
        else:
            return self.__sub_get_all()
    def get_option(self,name):
        self.option_name=unicode(name)
        r=self.__sub_get_option_name(self.option_name)
        if r.has_key("option_value"):
            self.option_value=r["option_value"]
            self.option_id=r["option_id"]
            try:rval=ast.literal_eval(self.option_value)
            except:rval=self.option_value
            return rval
        
        return None
    def get_option_value(self,*kwards,**kwargs):
        data=self.get(*kwards,**kwargs)
        if type(data)==dict:
            if data.has_key("option_value"):return data["option_value"]
        else:return ""
    
    def has_option(self,option_name):
        try:
            ins=self.s().query(OptionModel).filter(OptionModel.option_name==unicode(option_name)).first()
            if ins!=None:return True
            else:return False
        except Exception,e:
            self.derror(e)
            return False
        
    def has_option_id(self,option_id):
        try:
            ins=self.s().query(OptionModel).filter(OptionModel.option_id==option_id).first()
            if ins!=None:return True
            else:return False
        except Exception,e:
            self.derror(e)
            return False    
    
    def reset(self):
        self.option_id=None
        self.option_name=None
        self.option_value=None    
    
    def derror(self,e):
        if self.debug():
            print "## class:Option ##"
            print e
            print error()
            print "## -- ##"
        
    def s(self):return self.__sob.s()
    def debug_on(self):self.__d=True
    def debug_off(self):self.__d=False
    def debug(self):return self.__d
    def __repr__(self):return "<Option (option_id='%s')>"%(self.option_id)
###############################################









#########################################


## Movie info ##
class MovieModel(declarative_base()):
    """
    visibility:
        1=Shown
        0=Hidden
    """
    
    __tablename__="MovieDb"
    
    movie_id = Column(Integer,primary_key=True)#unique
    
    path = Column(Unicode)#unique #1
    
    
    
    imdbid = Column(Unicode,default=u"") #2
    imdbrating = Column(Float,default=0.0) #3
    year=Column(Integer,default=0) #4
    plot = Column(Unicode,default=u"") #5
    rated = Column(Unicode,default=u"") #6
    title = Column(Unicode,default=u"") #7
    poster = Column(Unicode,default=u"") #8
    writer = Column(Unicode,default=u"") #9
    director = Column(Unicode,default=u"") #10
    released = Column(Unicode,default=u"") #11
    actors = Column(Unicode,default=u"") #12
    genre = Column(Unicode,default=u"") #13
    runtime = Column(Unicode,default=u"") #14
    type = Column(Unicode,default=u"") #15
    imdbvotes = Column(Unicode,default=u"") #16
    
    


    
    visibility = Column(Integer,default=1) #17
    rating = Column(Float,default=0.0) #18
    tags = Column(Unicode,default=u"") #19
    
    others = Column(Unicode,default=u"{}")
    
    cdate = Column(DateTime,default=datetime.datetime.utcnow)
    udate = Column(DateTime)
    
    
    
    
    def __repr__(self):
        return "<MovieModel (movie_id='%s') (python_id='%s'>" %( self.movie_id , str( id(self) ) )
##


    
class Movie(object):
    def __init__(self,*kwards,**kwargs):
        self.__d=True
        self.__fields=["movie_id",
                       "path",#Unicode #1
                       
                       "imdbid",#Unicode #2
                       "imdbrating",#Float #3
                       "year",#Integer #4
                       "plot",#Unicode #5
                       "rated",#Unicode #6
                       "title",#Unicode #7
                       "poster",#Unicode #8
                       "writer",#Unicode #9
                       "director",#Unicode #10
                       "released",#Unicode #11
                       "actors",#Unicode #12
                       "genre",#Unicode #13
                       "runtime",#Unicode #14
                       "type",#Unicode #15
                       "imdbvotes",#Unicode #16
                       
                       "visibility",#Integer #17 #(1-Show,0-Hide) 
                       "rating",#Float #18
                       "tags"#Unicode #19
                       ]
        if len(kwards)==0:
            self.__sob=SOB(config.DB_MOVIE)
            self.__sob.set_model(MovieModel)
            
        if len(kwards)==1:
            self.__sob=kwards[0]
            if type(self.__sob)==SOB:
                self.__sob.set_model(MovieModel)
            elif type(self.__sob)==str:
                self.__sob=SOB(self.__sob)
                self.__sob.set_model(MovieModel)
        
    def get_fields(self):return self.__fields

    def has_movie_id(self,movie_id):
        try:
            s=self.s()
            movie_id=int(movie_id)
            ins=s.query(MovieModel).filter( MovieModel.movie_id == movie_id ).first()
            if ins==None:return False
            else:return True
        except Exception,e:
            self.derror(e)
            return False    
    
    def has_path(self,path):
        try:
            s=self.s()
            path=unicode(path)
            ins=s.query(MovieModel).filter( MovieModel.path == path ).first()
            if ins==None:return False
            else:return True
        except Exception,e:
            self.derror(e)
            return False
        
    def has_imdbid(self,imdbid):
        try:
            s=self.s()
            imdbid=unicode(imdbid)
            ins=s.query(MovieModel).filter( MovieModel.imdbid == imdbid ).first()
            if ins==None:return False
            else:return True
        except Exception,e:
            self.derror(e)
            return False
        
    def get_by_year(self,year,**kwargs):
        try:
            #print year
            s=self.s()
            q=s.query(MovieModel)
            year=int(year)
            q=q.filter(or_(MovieModel.year.like(year)
                           )
                       )
            nq=q
            if kwargs.has_key("o"):q=q.order_by(kwargs["o"])
            elif kwargs.has_key("order_by"):q=q.order_by(kwargs["order_by"])
            elif kwargs.has_key("order"):q=q.order_by(kwargs["order"])
            else:q=q.order_by("movie_id desc")
            
            i=0#i=1 iter#i=0 don't iter
            if kwargs.has_key("i"):
                try:i=int(kwargs["i"])
                except:pass
            
            #print i
            try:
                if i==1:data=q
                else:data=q.all()
            except:
                if i==1:data=nq
                else:data=nq.all()
            return data
                 
        except Exception,e:self.derror(e)
        return None

    def get_by_genre(self,genre,**kwargs):
        try:
            s=self.s()
            q=s.query(MovieModel)
            genre=unicode("%"+genre+"%")
            q=q.filter(or_(MovieModel.genre.like(genre)
                           )
                       )
            nq=q
            if kwargs.has_key("o"):q=q.order_by(kwargs["o"])
            elif kwargs.has_key("order_by"):q=q.order_by(kwargs["order_by"])
            elif kwargs.has_key("order"):q=q.order_by(kwargs["order"])
            else:q=q.order_by("movie_id desc")
            
            i=0#i=1 iter#i=0 don't iter
            if kwargs.has_key("i"):
                try:i=int(kwargs["i"])
                except:pass
            
            #print i
            try:
                if i==1:data=q
                else:data=q.all()
            except:
                if i==1:data=nq
                else:data=nq.all()
            return data
                 
        except Exception,e:self.derror(e)
        return None
    
    def get(self,*kwards,**kwargs):
        try:
            s=self.s()
            q=s.query(MovieModel)
            if len(kwards)==1:
                if type(kwards[0])==int:
                    movie_id=kwards[0]
                    #q=s.query(MovieModel)
                    q=q.filter(MovieModel.movie_id==movie_id)
                elif type(kwards[0])==str or type(kwards[0])==unicode:
                    try:
                        movie_id=int(kwards[0])
                        q=q.filter(MovieModel.movie_id==movie_id)
                    except:
                        path=unicode(kwards[0])
                        #q=s.query(MovieModel)
                        q=q.filter(MovieModel.path==path)
            elif kwargs.has_key("imdbid"):
                imdbid=unicode(kwargs["imdbid"])
                q=q.filter(MovieModel.imdbid==imdbid)
            elif kwargs.has_key("movie_id"):
                movie_id=int(kwargs["movie_id"])
                #q=s.query(MovieModel)
                q=q.filter(MovieModel.movie_id==movie_id)
            elif kwargs.has_key("path"):
                #q=s.query(MovieModel)
                path=unicode(kwargs["path"])
                q=q.filter(MovieModel.path==path)
            elif kwargs.has_key("search"):
                search=unicode(kwargs["search"])
                if search!=u"":
                    tag=unicode("%"+search+"%")
                    q=q.filter(or_(
                                   MovieModel.path.like(tag),
                                   MovieModel.plot.like(tag),
                                   MovieModel.title.like(tag),
                                   MovieModel.writer.like(tag),
                                   MovieModel.director.like(tag),
                                   MovieModel.actors.like(tag),
                                   MovieModel.genre.like(tag),
                                   MovieModel.tags.like(tag),
                                   MovieModel.others.like(tag)
                                   )
                               )
            nq=q
            if kwargs.has_key("o"):q=q.order_by(kwargs["o"])
            elif kwargs.has_key("order_by"):q=q.order_by(kwargs["order_by"])
            elif kwargs.has_key("order"):q=q.order_by(kwargs["order"])
            else:q=q.order_by("movie_id desc")
            
            i=0#i=1 iter#i=0 don't iter
            if kwargs.has_key("i"):
                try:i=int(kwargs["i"])
                except:pass
            
            #print i
            try:
                if i==1:data=q
                else:data=q.all()
            except:
                if i==1:data=nq
                else:data=nq.all()
            return data
                 
        except Exception,e:self.derror(e)
        return None      

    def get_by_tag(self,tag,*kwards,**kwargs):
        try:
            s=self.s()
            q=s.query(MovieModel)
            tag=unicode("%"+tag+"%")
            q=q.filter(or_(
                           MovieModel.tags.like(tag),
                           )
                       )
            nq=q
            if kwargs.has_key("o"):q=q.order_by(kwargs["o"])
            elif kwargs.has_key("order_by"):q=q.order_by(kwargs["order_by"])
            elif kwargs.has_key("order"):q=q.order_by(kwargs["order"])
            else:q=q.order_by("movie_id desc")
            
            i=0#i=1 iter#i=0 don't iter
            if kwargs.has_key("i"):
                try:i=int(kwargs["i"])
                except:pass
            
            #print i
            try:
                if i==1:data=q
                else:data=q.all()
            except:
                if i==1:data=nq
                else:data=nq.all()
            return data
                 
        except Exception,e:self.derror(e)
        return None
    
    
    def get_tags(self,*kwards,**kwargs):
        try:
            s=self.s()
            q=s.query(MovieModel)
            tags=[]
            for m in q:
                tag=m.tags
                if tag!="":
                    tag=tag.split(",")
                    tags.extend(tag)
            tags=list(set(tags))
            tags=map(string.lower,tags)
            tags=map(string.strip,tags)
            return tags                 
        except Exception,e:self.derror(e)
        return []
    
    def get_genre(self,*kwards,**kwargs):pass
    def get_writer(self,*kwards,**kwargs):pass
    def get_director(self,*kwards,**kwargs):pass
    def get_actors(self,*kwards,**kwargs):pass
    
    
    def add(self,*kwards,**kwargs):
        data=None
        try:
            s=self.s()
            #print s
            if len(kwards)==1:data=kwards[0]   
            if kwargs.has_key("data"):data=kwargs["data"]
            if type(data)!=dict:return False
            if data.has_key("path"):
                path=unicode(data["path"])
                if path==u"":return False
                ins=s.query(MovieModel).filter( MovieModel.path == path ).first()
                if ins==None:
                    ins=MovieModel()
                    others={}
                    for i in data.keys():
                        i=i.lower()
                        try:
                            self.__fields.index(i)
                            try:
                                if i=="imdbrating" or i=="rating":
                                    st="ins.%s=%s" %(i,float(data[i]))
                                    exec(st)
                                elif i=="year" or i=="visibility" or i=="movie_id":
                                    st="ins.%s=%s" %(i,int(data[i]))
                                    exec(st)
                                else:
                                    st='ins.%s=unicode(data["%s"])' %(i,i)
                                    exec(st)
                                    #print ins.path
                            except Exception,e:self.derror(e)
                        except:others[i]=data[i]
                        
                    try:
                        ins.others=unicode(str(others))
                        s.add(ins)
                        s.flush()
                        s.commit()
                        #try:Movie.MovieSignal.signal.emit("added",path)
                        #except:pass
                        return True
                    except Exception,e:self.derror(e)
                else:return False
        except Exception,e:self.derror(e)
        return False


    
    def update(self,*kwards,**kwargs):
        try:
            s=self.s()
            data=None
            if len(kwards)==1:
                data=kwards[0]
            if kwargs.has_key("data"):
                data=kwargs["data"]
            if type(data)!=dict:return False
            else:
                others={}
                for i in data.keys():
                    try:
                        self.__fields.index(i)
                        if i=="imdbrating" or i=="rating":
                            data[i]=float(data[i])
                        elif i=="year" or i=="visibility" or i=="movie_id":
                            data[i]=int(data[i])
                        else:
                            data[i]=unicode(data[i])
                    except:
                        others[i]=data[i]
                        del data[i]
                data["others"]=unicode(others)
                data["udate"]=datetime.datetime.utcnow()
                
                        
            if data.has_key("path"):
                path=data["path"]
                ins=s.query(MovieModel).filter( MovieModel.path == path ).first()
                if ins==None:return False
                
                s.query(MovieModel).filter(MovieModel.path==path).update(data)
            elif data.has_key("movie_id"):
                movie_id=data["movie_id"]
                #print movie_id
                ins=s.query(MovieModel).filter( MovieModel.movie_id == movie_id ).first()
                if ins==None:return False
                s.query(MovieModel).filter(MovieModel.movie_id==movie_id).update(data)
            else:
                return False
                
            try:
                #print "Commiting"
                s.commit()
                s.flush()
                #try:Movie.MovieSignal.signal.emit("updated",data["path"])
                #except:pass
                return True
            except:pass
        except Exception,e:self.derror(e)
        return False

    def rupdate(self,*kwards,**kwargs):
        try:
            s=self.s()
            data=None
            if len(kwards)==1:
                data=kwards[0]
            if kwargs.has_key("data"):
                data=kwargs["data"]
            if type(data)!=dict:return (False,None)
            else:
                others={}
                for i in data.keys():
                    try:
                        self.__fields.index(i)
                        if i=="imdbrating" or i=="rating":
                            data[i]=float(data[i])
                        elif i=="year" or i=="visibility" or i=="movie_id":
                            data[i]=int(data[i])
                        else:
                            data[i]=unicode(data[i])
                    except:
                        others[i]=data[i]
                        del data[i]
                data["others"]=unicode(others)
                data["udate"]=datetime.datetime.utcnow()
                
                        
            if data.has_key("path"):
                path=data["path"]
                ins=s.query(MovieModel).filter( MovieModel.path == path ).first()
                if ins==None:return (False,None)
                
                s.query(MovieModel).filter(MovieModel.path==path).update(data)
            elif data.has_key("movie_id"):
                movie_id=data["movie_id"]
                #print movie_id
                ins=s.query(MovieModel).filter( MovieModel.movie_id == movie_id ).first()
                if ins==None:return (False,None)
                s.query(MovieModel).filter(MovieModel.movie_id==movie_id).update(data)
            else:
                return (False,None)
                
            try:
                #print "Commiting"
                s.commit()
                s.flush()
                #print ins.tags
                #try:Movie.MovieSignal.signal.emit("updated",data["path"])
                #except:pass
                return (True,ins)
            except:pass
        except Exception,e:self.derror(e)
        return (False,None)

    
    def delete(self,*kwards,**kwargs):
        try:
            s=self.s()
            dm=None
            if len(kwards)==1:
                if type(kwards[0])==str or type(kwards[0])==unicode:
                    path=unicode(kwards[0])
                    dm=s.query(MovieModel).filter(MovieModel.path==path).one()
                elif type(kwards[0])==int:
                    movie_id=kwards[0]
                    dm=s.query(MovieModel).filter(MovieModel.movie_id==movie_id).one()
                else:return False
                    
            if kwargs.has_key("path"):
                path=unicode(kwargs["path"])
                dm=s.query(MovieModel).filter(MovieModel.path==path).one()
            if kwargs.has_key("movie_id"):
                movie_id=int(kwargs["movie_id"])
                dm=s.query(MovieModel).filter(MovieModel.movie_id==movie_id).one()
            if dm!=None:
                s.delete(dm)
                s.commit()
                #try:Movie.MovieSignal.signal.emit("deleted",path)
                #except:pass
                return True
                
        except Exception,e:self.derror(e)
        return False
    
    
    def add_tags(self,*kwards,**kwargs):
        if len(kwards)==2:
            m_p=kwards[0]
            tag=kwards[1]
            s=self.s()
            try:
                m_p=int(m_p)
                ins=s.query(MovieModel).filter(MovieModel.movie_id==m_p).one()
            except:
                try:
                    m_p=unicode(m_p)
                    ins=s.query(MovieModel).filter(MovieModel.path==m_p).one()
                except:ins=None
            if ins!=None:
                old_tags=ins.tags
                new_tags=old_tags.strip()
                tag_list=[]
                
                if type(tag)==str and tag!="" and tag!=None:
                    tag=unicode(tag)+","+new_tags
                    tag_list=tag.split(",")
                if type(tag)==list:
                    tag_list=new_tags.split(",")+tag
                    
                ntag=[]
                for i in tag_list:
                    i=i.strip()
                    if i!="":
                        try:ntag.index(i)
                        except:ntag.append(i)
                tags=",".join(ntag)
                ins.tags=tags
                
                try:
                    s.commit()
                    s.flush()
                    return True
                except:pass
        return False
                
            
    
    def map(self,obj_):
        if type(obj_)==MovieModel:return self.map_single(obj_)
        elif type(obj_)==list:
            lst=[]
            for i in obj_:lst.append(self.map_single(i))
            return lst
        else:
            return None
        
    def map_single(self,obj_):
        if type(obj_)==MovieModel:
            temp={}
            #others={}
            for i in self.__fields:
                #print i
                try:exec( 'temp["%s"]=obj_.%s' %(i,i) )
                except:pass
            try:others=ast.literal_eval(obj_.others)
            except:others={}
            temp["others"]=others
            temp["cdate"]=obj_.cdate
            temp["udate"]=obj_.udate
            return temp
            
    def derror(self,e):
        if self.debug():
            print "## class:Movie ##"
            print e
            print error()
            print "## -- ##"
    def v(self):self.__sob.vaccum()
    def s(self):return self.__sob.s()
    def debug_on(self):self.__d=True
    def debug_off(self):self.__d=False
    def debug(self):return self.__d
    def __repr__(self):return "<Option (python_id='%s')>"%( str(id(self)) )
            
            
        
    
        












## Meta info of movies  ##
class MovieMetaModel(declarative_base()):
    __tablename__="MovieMetaDb"
    meta_id=Column(Integer,primary_key=True)
    movie_id=Column(Integer)
    meta_key=Column(Unicode)
    meta_value=Column(Unicode)

    def __repr__(self):
        return "<MovieMetaModel (meta_id='%s')>"%(self.meta_id)
##


class MovieMeta(object):
    def __init__(self,*kwards,**kwargs):
        self.__d=True
        if len(kwards)==0:
            self.__sob=SOB(config.DB_MOVIE_META)
            self.__sob.set_model(MovieMetaModel)
            
        if len(kwards)==1:
            self.__sob=kwards[0]
            if type(self.__sob)==SOB:
                self.__sob.set_model(MovieMetaModel)
            elif type(self.__sob)==str:
                self.__sob=SOB(self.__sob)
                self.__sob.set_model(MovieMetaModel)
                
    def add(self,*kwards,**kwargs):
        try:
            s=self.s()
            if len(kwards)==3:
                movie_id=int(kwards[0])
                meta_key=unicode(kwards[1]).strip()
                meta_value=unicode(kwards[2]).strip()
                
                ins=s.query(MovieMetaModel).filter(MovieMetaModel.movie_id==movie_id)
                ins=ins.filter(MovieMetaModel.meta_key==meta_key).first()
                if ins==None:
                    if meta_key!=u"" and meta_value!=u"" and movie_id!=u"":
                        ins=MovieMetaModel()
                        ins.movie_id=movie_id
                        ins.meta_key=meta_key
                        ins.meta_value=meta_value
                        s.add(ins)
                        s.flush()
                        s.commit()
                        return True
        except:pass
        return False
    
    def delete(self,*kwards,**kwargs):
        #pass
        try:
            s=self.s()
            ins=None
            if len(kwards)==1:
                try:
                    meta_id=int(kwards[0])
                    ins=s.query(MovieMetaModel).filter(MovieMetaModel.meta_id==meta_id).one()
                except:pass
            
            if ins!=None:
                s.delete(ins)
                s.commit()
                return True
        except:pass
        return False
    
    
    def get(self,*kwards,**kwargs):
        try:
            s=self.s()
            ins=s.query(MovieMetaModel)
            if len(kwards)==1:
                try:
                    meta_id=int(kwards[0])
                    ins=ins.filter(MovieMetaModel.meta_id==meta_id)
                except:
                    try:
                        meta_key=unicode(kwards[0])
                        ins=ins.filter(MovieMetaModel.meta_key==meta_key)
                    except:pass
            if kwargs.has_key("movie_id"):
                try:
                    movie_id=int(kwargs["movie_id"])
                    ins=ins.filter(MovieMetaModel.movie_id==movie_id)
                except:pass
            if kwargs.has_key("meta_key"):
                try:
                    meta_key=unicode(kwargs["meta_key"])
                    ins=ins.filter(MovieMetaModel.meta_key==meta_key)
                except:pass
                
            if kwargs.has_key("o"):ins=ins.order_by(kwargs["o"])
            elif kwargs.has_key("order_by"):ins=ins.order_by(kwargs["order_by"])
            elif kwargs.has_key("order"):ins=ins.order_by(kwargs["order"])
            else:ins=ins.order_by("trash_id desc")
            
            if kwargs.has_key("i"):
                if int(kwargs["i"])==1:return ins
            else:return ins.all()
        
        except:pass
        return None
    

    def has_movie_id(self,movie_id):
        try:
            movie_id=int(movie_id)
            s=self.s()
            ins=s.query(MovieMetaModel).filter(MovieMetaModel.movie_id==movie_id).one()
            if ins!=None:return True
        except:pass
        return False
    
    def has_meta_id(self,meta_id):
        try:
            meta_id=int(meta_id)
            s=self.s()
            ins=s.query(MovieMetaModel).filter(MovieMetaModel.meta_id==meta_id).one()
            if ins!=None:return True
        except:pass
        return False
    
    def has_meta_key(self,meta_key):
        try:
            meta_key=unicode(meta_key)
            s=self.s()
            ins=s.query(MovieMetaModel).filter(MovieMetaModel.meta_key==meta_key).one()
            if ins!=None:return True
        except:pass
        return False
    
        
    
    
    
    ## CommoN ##
    def derror(self,e):
        if self.debug():
            print "## class:Movie ##"
            print e
            print error()
            print "## -- ##"
            
    def v(self):self.__sob.vaccum()
    def s(self):return self.__sob.s()
    def debug_on(self):self.__d=True
    def debug_off(self):self.__d=False
    def debug(self):return self.__d
    def __repr__(self):return "<Trash (python_id='%s')>"%( str(id(self)) )
    ## End CommoN ##
#####################################################################





## poster data ##
class PosterModel(declarative_base()):
    __tablename__="PosterDb"
    poster_id = Column(Integer,primary_key=True)
    movie_id = Column(Integer)
    poster_data=Column(Binary,default="")
    def __repr__(self):
        return "<PosterModel (movie_id='%s')>"%(self.movie_id)
##

class Poster(object):
    def __init__(self,*kwards,**kwargs):
        self.__d=True
        if len(kwards)==0:
            self.__sob=SOB(config.DB_POSTER)
            self.__sob.set_model(PosterModel)
            
        if len(kwards)==1:
            self.__sob=kwards[0]
            if type(self.__sob)==SOB:
                self.__sob.set_model(PosterModel)
            elif type(self.__sob)==str:
                self.__sob=SOB(self.__sob)
                self.__sob.set_model(PosterModel)
                
    def add(self,*kwards,**kwargs):
        try:
            s=self.s()
            if len(kwards)==2:
                movie_id=int(kwards[0])
                poster_data=int(kwards[1])
                if type(poster_data)==str:
                    if os.path.exists(poster_data):
                        try:poster_data=open(poster_data,"rb")
                        except:poster_data=None
                    else:poster_data=None
                data=None    
                if hasattr(poster_data,"read"):
                        data=""
                        for piece in util.read_in_chunks(poster_data):data=data+piece
                if hasattr(poster_data,"close"):poster_data.close()
                
                ins=s.query(PosterModel).filter(PosterModel.movie_id==movie_id).first()
                if ins==None and data!=None:
                    ins=PosterModel()
                    ins.movie_id=movie_id
                    ins.poster_data=data
                    
                    s.add(ins)
                    s.flush()
                    s.commit()
                    return True
        except:pass
        return False
    def delete(self,*kwards,**kwargs):
        #pass
        try:
            s=self.s()
            ins=None
            if len(kwards)==1:
                try:
                    poster_id=int(kwards[0])
                    ins=s.query(PosterModel).filter(PosterModel.poster_id==poster_id).one()
                except:pass
            
            
            if ins!=None:
                s.delete(ins)
                s.commit()
                return True
        except:pass
        return False
    
    
    def get(self,*kwards,**kwargs):
        try:
            s=self.s()
            ins=s.query(PosterModel)
            if len(kwards)==1:
                try:
                    poster_id=int(kwards[0])
                    ins=ins.filter(PosterModel.poster_id==poster_id)
                except:pass
            elif kwargs.has_key("movie_id"):
                try:
                    movie_id=int(kwargs["movie_id"])
                    ins=ins.filter(PosterModel.movie_id==movie_id)
                except:pass
            
            if kwargs.has_key("o"):ins=ins.order_by(kwargs["o"])
            elif kwargs.has_key("order_by"):ins=ins.order_by(kwargs["order_by"])
            elif kwargs.has_key("order"):ins=ins.order_by(kwargs["order"])
            else:ins=ins.order_by("poster_id desc")
            
            if kwargs.has_key("i"):
                if int(kwargs["i"])==1:return ins
            else:return ins.all()
        except:pass
        return None
    

    def has_movie_id(self,movie_id):
        try:
            movie_id=int(movie_id)
            s=self.s()
            ins=s.query(PosterModel).filter(PosterModel.movie_id==movie_id).one()
            if ins!=None:return True
        except:pass
        return False
    
    def has_poster_id(self,poster_id):
        try:
            poster_id=int(poster_id)
            s=self.s()
            ins=s.query(PosterModel).filter(PosterModel.poster_id==poster_id).one()
            if ins!=None:return True
        except:pass
        return False 
    
    
    ## CommoN ##
    def derror(self,e):
        if self.debug():
            print "## class:Movie ##"
            print e
            print error()
            print "## -- ##"
            
    def v(self):self.__sob.vaccum()
    def s(self):return self.__sob.s()
    def debug_on(self):self.__d=True
    def debug_off(self):self.__d=False
    def debug(self):return self.__d
    def __repr__(self):return "<Poster (python_id='%s')>"%( str(id(self)) )
    ## End CommoN ##
#####################################################################










## Trash ##
class TrashModel(declarative_base()):
    __tablename__="TrashDb"
    trash_id = Column(Integer,primary_key=True)
    path = Column(Unicode)
    def __repr__(self):
        return "<TrashModel (trash_id='%s')>"%(self.trash_id)
##

class Trash(object):
    def __init__(self,*kwards,**kwargs):
        self.__d=True
        if len(kwards)==0:
            self.__sob=SOB(config.DB_TRASH)
            self.__sob.set_model(TrashModel)
            
        if len(kwards)==1:
            self.__sob=kwards[0]
            if type(self.__sob)==SOB:
                self.__sob.set_model(TrashModel)
            elif type(self.__sob)==str:
                self.__sob=SOB(self.__sob)
                self.__sob.set_model(TrashModel)
                
    def add(self,*kwards,**kwargs):
        #print "In Trash Add"
        try:
            s=self.s()
            if len(kwards)==1:
                path=unicode(kwards[0])
                #print path
                ins=s.query(TrashModel).filter(TrashModel.path==path).first()
                if ins==None:
                    #print ins
                    ins=TrashModel()
                    ins.path=path
                    
                    s.add(ins)
                    s.flush()
                    s.commit()
                    return True
        except:pass
        return False
    
    def delete(self,*kwards,**kwargs):
        #pass
        try:
            s=self.s()
            ins=None
            if len(kwards)==1:
                try:
                    trash_id=int(kwards[0])
                    ins=s.query(TrashModel).filter(TrashModel.trash_id==trash_id).one()
                except:
                    try:
                        path=unicode(kwards[0])
                        ins=s.query(TrashModel).filter(TrashModel.path==path).one()
                    except:pass
            
            
            if ins!=None:
                s.delete(ins)
                s.commit()
                return True
        except:pass
        return False
    
    
    def get(self,*kwards,**kwargs):
        try:
            s=self.s()
            ins=s.query(TrashModel)
            if len(kwards)==1:
                try:
                    trash_id=int(kwards[0])
                    ins=ins.filter(TrashModel.trash_id==trash_id)
                except:
                    try:
                        path=unicode(kwards[0])
                        ins=ins.filter(TrashModel.path==path)
                    except:pass
            if kwargs.has_key("o"):ins=ins.order_by(kwargs["o"])
            elif kwargs.has_key("order_by"):ins=ins.order_by(kwargs["order_by"])
            elif kwargs.has_key("order"):ins=ins.order_by(kwargs["order"])
            else:ins=ins.order_by("trash_id desc")
            
            if kwargs.has_key("i"):
                if int(kwargs["i"])==1:return ins
            else:return ins.all()
        
        except:pass
        return None
    

    def is_deleted(self,path):
        try:
            path=unicode(path)
            s=self.s()
            ins=s.query(TrashModel).filter(TrashModel.path==path).one()
            if ins!=None:return True
        except:pass
        return False
    
    def has_path(self,path):return self.is_deleted(path)
    
    
    
    ## CommoN ##
    def derror(self,e):
        if self.debug():
            print "## class:Movie ##"
            print e
            print error()
            print "## -- ##"
            
    def v(self):self.__sob.vaccum()
    def s(self):return self.__sob.s()
    def debug_on(self):self.__d=True
    def debug_off(self):self.__d=False
    def debug(self):return self.__d
    def __repr__(self):return "<Trash (python_id='%s')>"%( str(id(self)) )
    ## End CommoN ##
#####################################################################

## Status Model ##
class StatusModel(declarative_base()):
    __tablename__="StatusDb"
    id = Column(Integer,primary_key=True)
    name = Column(Unicode)
    data=Column(Binary,default="")
    cdate = Column(DateTime,default=datetime.datetime.utcnow)
    udate = Column(DateTime)
    
    def __repr__(self):return "<StatusModel id='%s' name='%s' python_id='%s'>" %( self.id,self.name, str( id(self) ) )
##



class Status(object):
    def __init__(self,*kwards,**kwargs):
        self.__d=False
        if len(kwards)==0:
            self.__sob=SOB(config.DB_STATUS)
            self.__sob.set_model(StatusModel)
            
        if len(kwards)==1:
            self.__sob=kwards[0]
            if type(self.__sob)==SOB:
                self.__sob.set_model(StatusModel)
            elif type(self.__sob)==str:
                self.__sob=SOB(self.__sob)
                self.__sob.set_model(StatusModel)

    def update(self,name,data):
        s=self.s()
        self.name=unicode(name)
        self.data=data
        
        ins=s.query(StatusModel).filter(StatusModel.name==self.name).first()
        if ins!=None:
            ins.data=self.data
            ins.udate=datetime.datetime.utcnow()
        else:
            ins=StatusModel()
            ins.name=self.name
            ins.data=self.data
            ins.udate=datetime.datetime.utcnow()
        #print ins                  
        try:
            s.add(ins)
            s.flush()
            s.commit()
            return True
        except Exception,e:
            self.derror(e)
        return False
    def get(self,name):
        try:
            name=unicode(name)
            s=self.s()
            ins=s.query(StatusModel).filter(StatusModel.name==name).first()
            if ins!=None:return ins
        except:pass
        return None
    def has_status(self,name):
        try:
            name=unicode(name)
            s=self.s()
            ins=s.query(StatusModel).filter(StatusModel.name==name).one()
            if ins!=None:return True
        except:pass
        return False
    
    
    
    ## CommoN ##
    def derror(self,e):
        if self.debug():
            print "## class:Status ##"
            print e
            print error()
            print "## -- ##"
            
    def v(self):self.__sob.vaccum()
    def s(self):return self.__sob.s()
    def debug_on(self):self.__d=True
    def debug_off(self):self.__d=False
    def debug(self):return self.__d
    def __repr__(self):return "<Status (python_id='%s')>"%( str(id(self)) )
    ## End CommoN ##


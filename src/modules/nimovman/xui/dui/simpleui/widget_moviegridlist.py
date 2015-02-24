'''
Created on Aug 17, 2013

@author: KaWsEr
'''
import re
import os
import time
import shutil
import string
import threading
import webbrowser
import subprocess
import pickle
from glob import glob
from PySide import QtGui
from PySide import QtCore
from modules.nimovman.core import util
from modules.nimovman.core import Log
from modules.nimovman.core import error
from modules.nimovman.core import config
from modules.nimovman.core.config import asset
from modules.nimovman.core import standardsignal

from modules.nimovman.xui.dui.moviemenu import MovieMenu
from modules.nimovman.core.dbmodel import Option,Movie,Trash
from modules.nimovman.core.imd import get_imdbid
from modules.nimovman.core import imd
##iMovMan JOB
from modules.nimovman.core import immjob


##
from modules.nimovman.xui.dui import trashwindow

##
import tageditorwindow
from progressbar import ProgressBar
from tageditorwindow import TagEditor
from ratingwindow import RatingWindow,RatingUpdated
from propertieswindow import PropertiesWindow
from editwindow import MovieEditor,MovieEditorUpdated


#######################
SingleUpdateSignal=standardsignal.SignalUnicode()


#### Single Update Movie ####
def single_update(path,imdbid):
        __name="Single Updae"
        option=Option()
        movie=Movie()
        try:data_path,cover_path=util.find_cover_data_path()
        except:return False
        if data_path!=None:util.make_dirs(data_path)
        if cover_path!=None:util.make_dirs(cover_path)

        try:api=option.get_option("movie_api")
        except:api=config.C_DEFAULT_API
        
        
        try:
            path=unicode(path)
            mapi=__import__(api)
            try:obj_mapi=mapi.mApi()
            except:obj_mapi=None
            #print obj_mapi
            if obj_mapi!=None:
                movies=movie.get(path=path,i=1).all()
                for smovie in movies:
                    #print smovie.path
                    movie_name=""
                    movie_name_wext=os.path.basename(smovie.path)
                    movie_name=util.name_without_ext(movie_name_wext)
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
                    if os.path.exists(idata_path_old):
                        #data=self.form_dict(idata_path_old)
                        try:os.remove(idata_path_old)
                        except:pass
                        
                    if os.path.exists(idata_path_new):
                        #data=self.form_dict(idata_path_new)
                        try:os.remove(idata_path_new)
                        except:pass
                                            
                    try:cover_format=option.get_option("C_COVER_FORMAT")
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
                    if cfound:
                        try:os.remove(cp)
                        except:pass
                        cfound=False
                        
                    
                    if data==None:
                        try:data=obj_mapi.get(i=imdbid)
                        except:data=None
                    
                    #print icover_path,idata_path_new#data
                    #print data
                    if type(data)==dict:
                        if not os.path.exists(idata_path_new):
                            util.make_data(data,idata_path_new)
                        if cfound==False:
                            if data.has_key("poster"):
                                try:util.download_file(data["poster"], icover_path+".jpg")
                                except:pass
                        data=util.make_unique_dict(data)
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
                                    Log("Single Update").critical("While Updating genre %s-%s",e,error())
                            ngenlist=old+genlist
                            try:

                                if genreupdated:
                                    Log(__name).info("Updating Genres")
                                    opt.replace("option_genre", ngenlist)
                                    Log(__name).info("Genres Updated")
                                    #try:self.MovieUpdaterGenreUpdated.signal.emit()
                                    #except Exception,e:Log(self.__name).critical("While Sending Signal %s-%s",e,error())
                            except Exception,e:
                                Log(__name).critical("While Updating genre %s-%s",e,error())
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
                                        Log(__name).info("Updating Year")
                                        opt.replace("option_year", old)
                                        Log(__name).info("Year Updated")
                                        #try:MovieUpdaterYearUpdated.signal.emit()
                                        #except Exception,e:Log(self.__name).critical("While Sending Signal %s-%s",e,error())
                                except Exception,e:
                                    Log(__name).critical("While Updating year %s-%s",e,error())
                            except Exception,e:
                                Log(__name).critical("While Updating year %s-%s",e,error())
                        ## End of Year Update Logic ##
                            
                        
                        
                        ##Update Movie Data##    
                        if movie.update(data):#Data Updated Send The Notification
                            Log(__name).info("Movie Updated: "+movie_name_wext)
                            SingleUpdateSignal.signal.emit("Movie Updated: "+movie_name_wext)
                            #self.notify("Movie Updated: "+movie_name_wext)
                            #try:MovieUpdater.MovieUpdaterUpdates.signal.emit(unicode(data["path"]))
                            #except:Log(self.__name).critical("Signal Sending Error %s",error())
                            #try:MovieUpdater.MovieUpdaterFinished.signal.emit(True)
                            #except:Log(self.__name).critical("Signal Sending Error %s",error())
                            return True
                    #break
                
        except Exception,e:
            Log(__name).error("%s-%s",e,error())
        #exit(0)
        return False
####################################





class MovieItem(QtGui.QListWidgetItem):
    COUNTER=0
    def __init__(self,moviedbmodel,rating_sticker=True,year_sticker=True):
        MovieItem.COUNTER=MovieItem.COUNTER+1
        super(MovieItem,self).__init__(str(MovieItem.COUNTER))
        self.width=config.COVER_WIDTH/2
        self.height=config.COVER_HEIGHT/2
        
        #self.width=500
        #self.height=500
        self.setSizeHint(QtCore.QSize(self.width,self.height))
        self.update(moviedbmodel, rating_sticker, year_sticker)
        #self.setHidden()
        
    def get_title(self):return self.title    
    
    def update(self,moviedbmodel,rating_sticker,year_sticker):
        self.movie_data=moviedbmodel
        self.moviedbmodel=moviedbmodel
        self.path=moviedbmodel.path
        title=moviedbmodel.title
        has_cover=self.has_cover(self.path)


        self.rating_sticker=rating_sticker
        self.year_sticker=year_sticker
        
        if title=="":
            title=None
        if title==None:
            title=unicode(self.get_name_from_path(self.path))
        self.title=title
        self.setText(self.title)
        self.__key="title"
        self.__order="asc"
        
        if has_cover[0]==True:
            pix=QtGui.QPixmap(has_cover[1])
        elif has_cover[0]==False:
            pix=QtGui.QPixmap(asset("nocover.jpg"))
            
        self.pix=pix
        img=pix.scaled(self.width, self.height, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        self.img=img
        
        if self.rating_sticker and self.movie_data.imdbrating!=u"0.0":
            rect_width=30
            rect_height=30
            rbox=QtGui.QPixmap(asset("ratingbox.png"))
            rbox=rbox.scaled(rect_width,rect_height, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            painter=QtGui.QPainter(img)
            painter.setPen(QtCore.Qt.white)
            painter.drawPixmap(img.width()-rect_width,0,rbox)
            painter.setFont(QtGui.QFont("Arial", 12,QtGui.QFont.Bold))
            painter.drawText(img.width()-rect_width+4,rect_height/2+6, str(self.movie_data.imdbrating))
            painter.end()
        if self.year_sticker and self.movie_data.year!=u"0":
            year_rect=QtGui.QPixmap(img.width(),20)
            ypainter=QtGui.QPainter(year_rect)
            ypainter.setFont(QtGui.QFont("Arial", 12))
            ypainter.setBrush(QtGui.QColor(0,0,0))
            ypainter.drawRect(0,0,img.width(),20)
            ypainter.setPen(QtCore.Qt.white)
            ypainter.drawText(year_rect.rect(),QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter,str(self.movie_data.year))
            ypainter.end()
            
            painter=QtGui.QPainter(img)
            painter.setOpacity(0.6)
            painter.drawPixmap(0,img.height()-20,year_rect)
            painter.end()
        self.setIcon(img)
        
        
        tooltip="<font color='red'><b>Title: %s<b/></font><br/>"%title
        if self.movie_data.year!="" and self.movie_data.year!=None and self.movie_data.year!="N/A":
            tooltip=tooltip+"Year: %s<br/>"%(self.movie_data.year)

        if self.movie_data.rating!=0.0 and self.movie_data.rating!="" and self.movie_data.rating!=None and self.movie_data.rating!="N/A":
            tooltip=tooltip+"My Rating: %s<br/>"%(self.movie_data.rating)
        
        if self.movie_data.imdbrating!="" and self.movie_data.imdbrating!=None and self.movie_data.imdbrating!="N/A": 
            tooltip=tooltip+"IMDb Rating: %s<br/>"%(self.movie_data.imdbrating)


            
        if self.movie_data.imdbvotes!="" and self.movie_data.imdbvotes!=None and self.movie_data.imdbvotes!="N/A":
            tooltip=tooltip+"IMDb Votes: %s<br/>"%(self.movie_data.imdbvotes)
            
        if self.movie_data.genre!="" and self.movie_data.genre!=None and self.movie_data.genre!="N/A":
            tooltip=tooltip+"Genre: %s<br/>"%self.movie_data.genre
            
        if self.movie_data.plot!="" and self.movie_data.plot!=None and self.movie_data.plot!="N/A":
            tooltip=tooltip+"<br/>"
            plot=self.movie_data.plot.split(" ")
            total_string=""
            
            temp=[]
            counter=0
            for i in plot:
                temp.append(i)
                counter=counter+len(i)
                if counter>=40:
                    total_string=total_string+"<br/>"+" ".join(temp)
                    temp=[]
                    counter=0
                #else:temp.append(i)
            if len(temp)!=0:total_string=total_string+"<br/>"+" ".join(temp)
                
                
            tooltip=tooltip+"Plot: %s"%(total_string)
        self.setToolTip(tooltip)
            
            
    def get_name_from_path(self,path):
        path=path
        if path.find("/")!=-1:path=path.split("/")[-1]
        elif path.find("\\")!=-1:path= path.split("\\")[-1]
        path=path.replace("."+path.split(".")[-1],"")
        return path
                
    def has_cover(self,path):
        option=Option()
        try:cover_format=option.get_option("C_COVER_FORMAT")
        except:cover_format=config.C_COVER_FORMAT
        
        #print icover_path
        name=os.path.basename(path).replace(path.split(".")[-1],"")
        _,cover_path=util.find_cover_data_path()
        if cover_path!=None:icover_path=os.path.join(cover_path,name)
        else:icover_path=path.replace(path.split(".")[-1],"")
            
        cfound=False
        for cf in cover_format:
            cp=icover_path+cf.lower()
            if os.path.exists(cp):
                cfound=True
                return (cfound,cp)
                break
        return (cfound,None)
    
    def setKey(self,key):self.__key=key
    def setOrder(self,order):self.__order=order
    def setAsc(self):self.__order="asc"
    def setDesc(self):self.__order="desc"
    
    
    def __lt__(self, other):
        
        if self.__key=="title" and self.__order=="asc":
            return self.title < other.title#ok
            
        
        elif self.__key=="title" and self.__order=="desc":
            return self.title > other.title#ok
            
        ####
        if self.__key=="year" and self.__order=="asc":
            return self.movie_data.year < other.movie_data.year
        
        elif self.__key=="year" and self.__order=="desc":
            return self.movie_data.year > other.movie_data.year
        ####
        if self.__key=="imdbrating" and self.__order=="asc":
            return self.movie_data.imdbrating < other.movie_data.imdbrating
        elif self.__key=="imdrating" and self.__order=="desc":
            return self.movie_data.imdbrating > other.movie_data.imdbrating
        ####
        if self.__key=="rating" and self.__order=="asc":
            return self.movie_data.rating < other.movie_data.rating
        elif self.__key=="rating" and self.__order=="desc":
            return self.movie_data.rating > other.movie_data.rating
        ####
        if self.__key=="oldest" and self.__order=="asc":
            return self.movie_data.cdate < other.movie_data.cdate
        elif self.__key=="oldest" and self.__order=="desc":
            return self.movie_data.cdate > other.movie_data.cdate
        
        return self.movie_data.imdbrating > other.movie_data.imdbrating
    
    
    
    
    
    
    def __repr__(self):return "<MovieItem '%s'>"%self.title
##########################################################################################



class MovieItemDeligate(QtGui.QStyledItemDelegate):
    def __init__(self,parent):
        super(MovieItemDeligate,self).__init__(parent)
        self.width=config.COVER_WIDTH/2
        self.height=config.COVER_HEIGHT/2
        self.padding=2
    
    def paintt(self,painter,option,index):
        #print painter
        #print option
        #print index
        #print option.state
        #print option.rect
        painter.drawText(option.rect,QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter,"Hi")
    
    def sizeHint(self,option,index):
        return QtCore.QSize(self.width,self.height)
############################################################################################













class MovieItemUpdater(threading.Thread):
    MovieItemUpdaterSignal=standardsignal.SignalInt()
    def __init__(self):
        super(MovieItemUpdater,self).__init__()
        self.__name="MovieItemUpdater"
        #self.signal=signal
        self.setDaemon(True)
        self.setName(self.__name)
        self.loop=True
        self.loops=0
        imd.MovieAdder.MovieAdderUpdates.signal.connect(self.movie_adder_updates)
        #self.movie=Movie()
        #self.movies=self.movie.get()
        #self.rowCount=len(self.movies)
        #self.index=0
        #self.data=None
        #self.fetched=0
        self.fetch_count=5
        self.reset()
        

    def movie_adder_updates(self,path):
        movieo=Movie()
        movie=movieo.get(path=path)[0]
        self.movies.append(movie)
        self.rowCount=len(self.movies)
    def fetchMore(self):
        remainder = self.rowCount - self.fetched
        itemsToFetch = min(self.fetch_count, remainder)
        data=self.movies[self.fetched:self.fetched+itemsToFetch]
        self.fetched += itemsToFetch
        #print self.fetched
        return data
        
    def isFetchFinished(self):return self.fetched==self.rowCount
               
    def next(self):
        if self.index<=self.rowCount:
            self.data=self.movies[self.index]
            self.index=self.index+1
            return self.data
        return None
    def current(self):return self.data
            
    def run(self):
        #time.sleep(2)
        while self.loop:
            if self.fetched<self.rowCount:
                #signal.emit(self.fetched)
                MovieItemUpdater.MovieItemUpdaterSignal.signal.emit(self.fetched)
                time.sleep(0.1)
            elif self.fetched==self.rowCount:
                #print self.lastSignal
                if self.lastSignal:
                    self.lastSignal=False
                    MovieItemUpdater.MovieItemUpdaterSignal.signal.emit(self.fetched)
            #break
    def reset(self):
        self.lastSignal=True
        movie=Movie()
        self.movies=movie.get()
        self.rowCount=len(self.movies)
        #print "Total Movies:",self.rowCount
        self.index=0
        self.data=None
        self.fetched=0
        
    def movie_by_genre(self,genre):
        self.lastSignal=True
        movie=Movie()
        self.movies=movie.get_by_genre(genre)
        self.rowCount=len(self.movies)
        #print "Total Movies:",self.rowCount
        self.index=0
        self.data=None
        self.fetched=0
        
    def movie_by_year(self,year):
        self.lastSignal=True
        movie=Movie()
        self.movies=movie.get_by_year(year)
        self.rowCount=len(self.movies)
        #print "Total Movies:",self.rowCount
        self.index=0
        self.data=None
        self.fetched=0
        
    def movie_by_tag(self,tag):
        self.lastSignal=True
        movie=Movie()
        self.movies=movie.get_by_tag(tag)
        self.rowCount=len(self.movies)
        #print "Total Movies:",self.rowCount
        self.index=0
        self.data=None
        self.fetched=0


    def movie_search(self,tag):
        self.lastSignal=True
        movie=Movie()
        self.movies=movie.get(search=tag)
        self.rowCount=len(self.movies)
        #print "Total Movies:",self.rowCount
        self.index=0
        self.data=None
        self.fetched=0









####
class MovieGridList(QtGui.QWidget):
    update_signal=standardsignal.MessageSendU()
    UpdateItem=standardsignal.IntUnicode()
    LoadStart=standardsignal.Signal()
    def __init__(self,parent):
        self.__name="MovieGridList"
        
        super(MovieGridList,self).__init__(parent)
        ###Stickers###
        self.rating_sticker=True
        self.year_sticker=True
        self.setObjectName(self.__name)
        self.setStyleSheet("""
        QWidget#MovieGridList{
        background-color: white;
        }
        """)
        self.setContentsMargins(0,0,0,0)

        self.main_layout=QtGui.QGridLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.vparent=parent
        self.imd=self.vparent.imd
        #print self.imd
        self.tool_bar=QtGui.QToolBar(self)
        self.tool_bar.setObjectName("iToolBar")
        self.tool_bar.setStyleSheet("""
        QToolBar#iToolBar{
         background: #ededed url(data/zimmlib/assets/bg_fallback.png) 0 0 repeat-x; 
         /*background-color: white;*/
         border-width: 0px;
        }
        """)
        self.tool_bar.setContentsMargins(0,0,0,0)
        
        
        
        self.search_bar=QtGui.QLineEdit(self)
        self.search_bar.setContentsMargins(0,0,0,0)
        self.search_bar.setContentsMargins(2,2,2,2)
        self.search_bar.setStyleSheet("""
        QLineEdit {
        background-color: white;
        color: black;
        selection-color: black;
        selection-background-color: #a0ddff;
        border-style: outset;
        /*border-width: 2px;*/
        border-radius: 3px;
        /*border-color: beige;*/
        
        }
        
        QLineEdit:hover:enabled { 
        background-color: #fffdb7;
        border: 1px solid #a2e1e5;
        
        }
        """)
        self.search_bar.setMaximumWidth(300)
        self.search_bar.setMinimumHeight(25)
        self.search_bar.textChanged.connect(self.search_bar_text_changed)
        
        self.tool_bar.addWidget(self.search_bar)
        #self.main_layout.addWidget(self.search_bar,0,0)
        self.main_layout.addWidget(self.tool_bar,0,0)


        self.movie_list=QtGui.QListWidget(self)
        self.movie_list.setContentsMargins(0,0,0,0)
        self.movie_list.setItemDelegate(MovieItemDeligate(self.movie_list))
        self.movie_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        #self.movie_list.setContentsMargins(100,100,100,100)
        #k=QtGui.QTableWidget()
        #k.setMode
        #self.movie_list.items()
        
        self.movie_list.setViewMode(QtGui.QListWidget.IconMode)
        #self.movie_list.setViewMode(QtGui.QListWidget.ListMode)
        #self.movie_list.setLayoutMode(QtGui.QListWidget.Batched)
        self.movie_list.setIconSize(QtCore.QSize(135,135))
        self.movie_list.setResizeMode(QtGui.QListWidget.ResizeMode.Adjust)
        self.movie_list.setDragEnabled(False)
        self.movie_list.setSortingEnabled(True)
        self.movie_list.doubleClicked.connect(self.dblclicked)
        self.movie_list.itemSelectionChanged.connect(self.selectedItems)
        #self.movie_list.ite
        
        
        
        #self.movie_list.itemActivated.connect(self.itemActivated)
        #self.movie_list.itemEntered.connect(self.itemEntered)


        self.main_layout.addWidget(self.movie_list,1,0)

        self.setLayout(self.main_layout)
        self.movie_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.movie_list.customContextMenuRequested.connect(self.contextMenuEvent)
        #self.movie_list.selection
        #self.movie_list.setUpdatesEnabled(False)
        #self.movie_list.up

        
        
        
        
        
        
        
        

        
        #self.movieitemupdater=MovieItemUpdater()
        #MovieItemUpdater.MovieItemUpdaterSignal.signal.connect(self.add_movie)
        
        #self.movieitemupdater.start()
        self.spin_start()
        
        self.update_signal.signal.connect(self.update_signal_call)
        
        ###Afte Multiple delete What to do
        #MoviesMenu.MoviesMenuMultipleDeleteStatus.signal.connect(self.movies_menu_multiple_delete_signal_handle)
        #MoviesMenu.MoviesMenuDeletedPath.signal.connect(self.movies_menu_deleted_path_handle)
        
        
        
        
        
        
        
        
        
        #########Initilize Everything Here############

        
        
        ### Widget Triggers ####
        #currentTextChanged
        self.vparent.genre_list.currentTextChanged.connect(self.genre_changed)
        self.vparent.year_list.currentTextChanged.connect(self.year_changed)
        self.vparent.tag_list.currentTextChanged.connect(self.tag_changed)
        
        #####MovieListConditionTracker#####
        self.year=None
        self.genre=None
        self.tag=None
        self.sortby="title"
        self.order="asc"
        self.__MOVIE_ITEMS__={}
        
        ##connect signal to a method##
        self.UpdateItem.signal.connect(self.update_item)
        SingleUpdateSignal.signal.connect(self.add_msg)
        
        
        
        
        ######Load All Movies To View###############
        #self.load_movies_to_view()
        self.LoadStart.signal.connect(self.load_movies_to_view)
        #self.LoadStart.signal.emit()
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.timeout)
        self.timer.start(1000)
        self.spin_start()


        ###Signal Receivers###
        self.movie_menu_signal_receivers_init()
        self.imd_signal_receivers_init()
        self.others_signal_receivers_init()
        RatingUpdated.signal.connect(self.imd_movie_updates)
        MovieEditorUpdated.signal.connect(self.imd_movie_updates)
    
    
    def timeout(self):
        self.timer.stop()
        self.LoadStart.signal.emit()
        
    def spin_start(self):self.vparent.update_signal.signal.emit("spin","start")
    def spin_stop(self):self.vparent.update_signal.signal.emit("spin","stop")
    def add_msg(self,msg):self.vparent.add_msg(msg)
        
        
    def search_bar_text_changed(self,text):
        #print text
        if len(text)>=0:
            #self.__MOVIE_ITEMS__={}
            #self.movie_list.clear()
            #self.movieitemupdater.movie_search(text)
            self.make_movies_visible_to_view(search=text)
        
    def genre_changed(self,genre):
        if genre.lower()!="all":
            matchObj  = re.match(r"^(.*) \((\d+)\)", genre, re.M|re.I)
            if matchObj:
                self.genre = matchObj.group(1)
                if self.genre.lower() == "all":
                    self.vparent.update_signal.signal.emit("status","Genre : "+self.genre)
                    self.make_all_movies_visible_to_view()
                else:
                    self.vparent.update_signal.signal.emit("status","Genre : "+self.genre)
                    self.make_movies_visible_to_view(genre=self.genre)
        else:
            self.genre = genre
            self.vparent.update_signal.signal.emit("status","Genre : "+self.genre)
            self.make_all_movies_visible_to_view()
        
            
    def tag_changed(self,tag):
        if tag.lower()!="all" and tag!=" ":
            matchObj  = re.match(r"^(.*) \((\d+)\)", tag, re.M|re.I)
            if matchObj:
                tag = matchObj.group(1)
                self.tag = tag
            if tag.lower()=="unwatched":
                self.vparent.update_signal.signal.emit("status","Tag : "+tag)
                self.make_movies_visible_to_view(exclude="watched")
            else:
                self.tag =tag
                self.vparent.update_signal.signal.emit("status","Tag : "+tag)
                self.make_movies_visible_to_view(tags=tag)
        else:
            self.vparent.update_signal.signal.emit("status","Tag : "+tag)
            self.make_all_movies_visible_to_view()
        
    def year_changed(self,year):
        if year.lower()!="all":
            matchObj  = re.match(r"^(.*) \((\d+)\)", year, re.M|re.I)
            if matchObj:
                self.year = matchObj.group(1)
                self.vparent.update_signal.signal.emit("status","Year: "+self.year)
                self.make_movies_visible_to_view(year=self.year)
        else:
            self.year = year
            self.vparent.update_signal.signal.emit("status","Year: "+year)
            self.make_all_movies_visible_to_view()


    def make_all_movies_visible_to_view(self):
        for path in self.__MOVIE_ITEMS__.keys():
            item=self.__MOVIE_ITEMS__[path]
            if item.isHidden():
                item.setHidden(False)

    def make_movies_visible_to_view(self,**kwargs):
        year=None
        genre=None
        tags=None
        search=None
        exclude=None
        
        if kwargs.has_key("year"):
            try:year=int(kwargs["year"])
            except:pass
            
        if kwargs.has_key("genre"):
            genre=kwargs["genre"]
            genre=genre.lower()
            
        if kwargs.has_key("tags"):
            tags=kwargs["tags"]
            tags=tags.lower()
            
        if kwargs.has_key("search"):
            search=kwargs["search"]
            search=search.lower()
            
        if kwargs.has_key("exclude"):
            exclude = kwargs["exclude"]
            exclude = exclude.lower()
            
  
        for path in self.__MOVIE_ITEMS__.keys():
            item=self.__MOVIE_ITEMS__[path]
            if year!=None:
                if item.movie_data.year!=year:item.setHidden(True)
                else:item.setHidden(False)
            if genre!=None:
                if item.movie_data.genre.lower().find(genre)==-1:item.setHidden(True)
                else:item.setHidden(False)
            if tags!=None:
                if item.movie_data.tags.lower().find(tags)==-1:item.setHidden(True)
                else:item.setHidden(False)
                            
            if exclude!=None:
                if item.movie_data.tags.lower().find(exclude)==-1:item.setHidden(False)
                else:item.setHidden(True)
                
            
            
            if search!=None:
                data=item.movie_data
                etitle=data.title.lower().find(search)!=-1
                efpath=data.path.lower().find(search)!=-1
                etags=data.tags.lower().find(search)!=-1
                egenre=data.genre.lower().find(search)!=-1
                eplot=data.plot.lower().find(search)!=-1
                edirector=data.director.lower().find(search)!=-1
                ewriter=data.writer.lower().find(search)!=-1
                eactors=data.actors.lower().find(search)!=-1
                eothers=data.others.lower().find(search)!=-1
                
                
                if etitle or efpath or etags or egenre or eplot or edirector or ewriter or eactors or eothers:
                    item.setHidden(False)
                else:
                    item.setHidden(True)
                
                
                
                    
                    


            
        

            

        
        
        
        
    def selectedItems(self,*kwards,**kwargs):
        #print self.movie_list.width(),self.movie_list.height()
        #print dir(self.movie_list.selectedItems()[0])
        #self.movie_list.d
        #self.movie_list.selectedItems()[0].title="Kawse"
        #self.movie_list.update()
        self.selected_ids=[k.row() for k in self.movie_list.selectedIndexes()]
        self.selected_paths=[k.path for k in self.movie_list.selectedItems()]
        #print self.selected_paths
        #print self.__MOVIE_ITEMS__
        #pixmap=QtGui.QPixmap(self.movie_list.size())
        
        #widget->render(&pixmap, QPoint(), QRegion(rectangle));
        #rect=QtCore.QRect(self.movie_list.rect())
        #rect.setHeight(2000)
        #self.movie_list.render(pixmap,QtCore.QPoint(),QtGui.QRegion(rect))
        
        #item=self.movie_list.selectedItems()[0]
        #item.setHidden(True)
        
        
        #pixmap.save("kawser.png")
        total_movies=len(self.movie_list.selectedItems())
        
        if total_movies>1:
            self.vparent.update_signal.signal.emit("status","Selected Movies: %s"%total_movies)
    
        
    def update_signal_call(self,itype,text):
        if itype=="update_movie_by_genre":
            self.vparent.update_signal.signal.emit("status","Genre : "+text)
            self.movie_by_genre(text)
        elif itype=="update_movie_by_year":
            self.vparent.update_signal.signal.emit("status","Year: "+text)
            self.movie_by_year(text)
        elif itype=="refresh":
            self.refresh_action()

            
            

    
    
        
    def add_movie(self,action):
        #print action
        #if action==0:
            #print "adding:",action
            self.spin_start()
            #self.movie_list.blockSignals(True)
            #self.movie_list.updatesEnabled(False)
            #self.movie_list.setUpdatesEnabled(False)
            datas=self.movieitemupdater.fetchMore()
            if not self.movieitemupdater.isFetchFinished():
                if self.movie_list.updatesEnabled():
                    pass#self.movie_list.setUpdatesEnabled(False)
            else:
                if not self.movie_list.updatesEnabled():
                    pass#self.movie_list.setUpdatesEnabled(True)
                self.spin_stop()
                
            #datas=self.movieitemupdater.movies
            #print datas
            if type(datas)==list:
                #self.movie_list.setUpdatesEnabled(False)
                #QtGui.QApplication.processEvents()
                for data in datas:
                    try:
                        mitem=MovieItem(data)
                        self.__MOVIE_ITEMS__[mitem.path]=mitem
                        self.movie_list.addItem(mitem)
                    except Exception,e:
                        Log(self.__name).critical("Add Movie: %s-%s",e,error())

                
    def contextMenuEvent(self, event):self.create_context_menu()
    def refresh_action(self):
        self.year=None
        self.genre=None
        self.tag=None
        self.movie_list.clear()
        self.load_movies_to_view()




#####################################################################
    def others_signal_receivers_init(self):
        tageditorwindow.TagUpdates.signal.connect(self.update_movie_of_view)
        
    def imd_signal_receivers_init(self):
        imd.MovieAdder.MovieAdderUpdates.signal.connect(self.add_movie_to_view)
        imd.MovieUpdater.MovieUpdaterUpdates.signal.connect(self.imd_movie_updates)
        imd.MovieRemover.MovieRemoverUpdates.signal.connect(self.delete_movie_from_view)
        
#####################################################################
    def movie_menu_signal_receivers_init(self):
        MovieMenu.SelectedDrive.signal.connect(self.movie_menu_selected_drive)
        MovieMenu.Sortby.signal.connect(self.movie_menu_sortby)
        
#####################################################
    def load_movies_to_view(self):
        self.spin_start()
        movie=Movie()
        movies=movie.get()
        for data in movies:
            mitem=MovieItem(data)
            self.__MOVIE_ITEMS__[mitem.path]=mitem
            QtGui.QApplication.processEvents()
            self.movie_list.addItem(mitem)
        self.spin_stop()

    def add_movie_to_view(self,path):
        movie=Movie()
        movies=movie.get(path=path)
        for data in movies:
            mitem=MovieItem(data)
            self.__MOVIE_ITEMS__[mitem.path]=mitem
            QtGui.QApplication.processEvents()
            self.movie_list.addItem(mitem)
            
        
    def delete_movie_from_view(self,path):
        """This method will delete movie from movie list (qlistwidget) view"""
        item=self.__MOVIE_ITEMS__[path]
        index=self.movie_list.indexFromItem(item).row()
        self.movie_list.takeItem(index)
        try:del self.__MOVIE_ITEMS__[item.path]
        except:pass
        
    def update_movie_of_view(self,path):
        """Do Something With updated Movie"""
        item=self.__MOVIE_ITEMS__[path]
        index=self.movie_list.indexFromItem(item)
        self.UpdateItem.signal.emit(index.row(),path)  
        
    def imd_movie_updates(self,path):
        """Do Something With updated Movie"""
        item=self.__MOVIE_ITEMS__[path]
        index=self.movie_list.indexFromItem(item)
        self.UpdateItem.signal.emit(index.row(),path)    
#####################################################










#####################################################
    def dblclicked(self,index):
        try:
            k=self.movie_list.itemFromIndex(index)
            Log(self.__name).info("Play initiating : %s",k.path)
            if hasattr(immjob,"file_play"):immjob.file_play(k.path)
            else:Log(self.__name).error("file_play function not found")
        except Exception,e:
            Log(self.__name).critical("DblClicked : %s-%s",e,error())
  
    def single_update_movie(self,item_id,imdbid):
        ProgressBar.ProgressStarted.signal.emit(1)
        try:
            item=self.movie_list.item(item_id)
            path=item.path
            ProgressBar.ProgressMessage.signal.emit("Updating: %s"%item.get_title())
            ustatus=single_update(item.path,imdbid)
            if ustatus:
                #self.update_item(item_id,path)
                self.UpdateItem.signal.emit(item_id,path)
                ProgressBar.ProgressReport.signal.emit(1)
        except:pass
        ProgressBar.ProgressFinished.signal.emit(True)
    
    def progress_check(self,*kwards,**kwargs):
        ProgressBar.ProgressStarted.signal.emit(100)
        for i in xrange(100):
            time.sleep(0.5)
            #print i
            ProgressBar.ProgressMessage.signal.emit(str(i))
            ProgressBar.ProgressReport.signal.emit(i)

        ProgressBar.ProgressFinished.signal.emit(True)
    
    
    def update_item(self,number,path):
        try:
            #print number
            #number=int(number)
            movieo=Movie()
            movie=movieo.get(path=path)[0]
            self.movie_list.item(number).update(movie,self.year_sticker,self.rating_sticker)
        except Exception,e:
            Log(self.__name).critical("Error in update item %s %s",error(),e)
    

        
    
    
    def delete_movies(self,*kwards,**kwargs):
        ProgressBar.ProgressStarted.signal.emit(100)
        try:
            ids=kwards[0]
            #print ids
            count=1
            ProgressBar.ProgressStarted.signal.emit(len(ids))
            ids.sort()
            ids.reverse()
            trash=Trash()
            movie=Movie()
            for sid in ids:
                try:
                    item=self.movie_list.item(sid)
                    ProgressBar.ProgressMessage.signal.emit("Deleting: %s"%item.get_title())
                    tadd=trash.add(item.path)
                    Log(self.__name).info("Trash Add %s: %s",item.path,tadd)
                    mdel=movie.delete(item.path)
                    Log(self.__name).info("Movie Delete %s: %s",item.path,mdel)
                    self.movie_list.takeItem(sid)
                    trashwindow.TrashWindow.TrashDataReset.signal.emit(1)
                    ProgressBar.ProgressReport.signal.emit(count)
                    count=count+1
                    try:del self.__MOVIE_ITEMS__[item.path]
                    except:pass
                except:
                    Log(self.__name).critical("Deleting Error: %s",error())
        except:Log(self.__name).critical("Deleting Error %s",error())
        ProgressBar.ProgressFinished.signal.emit(True)
            
    def make_favourite(self,*kwards,**kwargs):
        ProgressBar.ProgressStarted.signal.emit(100)
        try:
            items=kwards[0]
            act=kwards[1]
            count=1
            ProgressBar.ProgressStarted.signal.emit(len(items))
            #print act
            for item in items:
                try:
                    movieo=Movie()
                    movie=movieo.get(path=item.path)
                    tags=movie[0].tags
                    #print "Tags:",tags
                    if tags==u"":
                        tags=[]
                    else:
                        tags=tags.lower()
                        tags=tags.split(",")
                        tags=map(string.strip,tags)
                        
                    #print movie
                    #tags=tags.lower()
                    #print act
                    #tags=tags.split(",")
                    #print act
                    #print "Tags"
                    #print self.movie_list.indexFromItem(item).row()
                    if act=="favourite":
                        ProgressBar.ProgressMessage.signal.emit("Making %s Favourite"%item.get_title())
                        if "favourite" not in tags:
                            tags.append("favourite")
                            data={"path":item.path,"tags":",".join(tags)}
                            datar=movieo.rupdate(data)
                            #print self.movie_list.indexFromItem(item).row()
                            if datar[0]:
                                self.UpdateItem.signal.emit(self.movie_list.indexFromItem(item).row(),item.path)
                    if act=="unfavourite":
                        ProgressBar.ProgressMessage.signal.emit("Removing %s From Favourite"%item.get_title())
                        if "favourite" in tags:
                            try:del tags[tags.index("favourite")]
                            except:pass
                            data={"path":item.path,"tags":",".join(tags)}
                            datar=movieo.rupdate(data)
                            if datar[0]:
                                self.UpdateItem.signal.emit(self.movie_list.indexFromItem(item).row(),item.path)
                                
                    #ProgressBar.ProgressMessage.signal.emit(item.path)
                except:pass
                
                ProgressBar.ProgressReport.signal.emit(count)
                count=count+1
        except:pass
        #self.refresh_action()
        ProgressBar.ProgressFinished.signal.emit(True)
        

    def make_wish_list(self,*kwards,**kwargs):
        ProgressBar.ProgressStarted.signal.emit(100)
        try:
            items=kwards[0]
            act=kwards[1]
            count=1
            ProgressBar.ProgressStarted.signal.emit(len(items))
            #print act
            for item in items:
                try:
                    
                    #print item
                    movieo=Movie()
                    movie=movieo.get(path=item.path)
                    tags=movie[0].tags
                    #print "Tags:",tags
                    if tags==u"":
                        tags=[]
                    else:
                        tags=tags.lower()
                        tags=tags.split(",")
                        tags=map(string.strip,tags)
                        
                    #print movie
                    #tags=tags.lower()
                    #print act
                    #tags=tags.split(",")
                    #print act
                    #print "Tags"
                    #print self.movie_list.indexFromItem(item).row()
                    if act=="wish list":
                        ProgressBar.ProgressMessage.signal.emit("Adding %s into Wish List"%item.get_title())
                        if "wish list" not in tags:
                            tags.append("wish list")
                            data={"path":item.path,"tags":",".join(tags)}
                            datar=movieo.rupdate(data)
                            #print self.movie_list.indexFromItem(item).row()
                            if datar[0]:
                                self.UpdateItem.signal.emit(self.movie_list.indexFromItem(item).row(),item.path)
                    if act=="remove from wish list":
                        ProgressBar.ProgressMessage.signal.emit("Removing %s From Wish List"%item.get_title())
                        if "wish list" in tags:
                            try:del tags[tags.index("wish list")]
                            except:pass
                            data={"path":item.path,"tags":",".join(tags)}
                            datar=movieo.rupdate(data)
                            if datar[0]:
                                self.UpdateItem.signal.emit(self.movie_list.indexFromItem(item).row(),item.path)
                                
                    #ProgressBar.ProgressMessage.signal.emit(item.path)
                except:pass
                
                ProgressBar.ProgressReport.signal.emit(count)
                count=count+1
        except:pass
        #self.refresh_action()
        ProgressBar.ProgressFinished.signal.emit(True)
        
    def make_watch_list(self,*kwards,**kwargs):
        ProgressBar.ProgressStarted.signal.emit(100)
        try:
            items=kwards[0]
            act=kwards[1]
            count=1
            ProgressBar.ProgressStarted.signal.emit(len(items))
            #print act
            for item in items:
                try:
                    
                    #print item
                    movieo=Movie()
                    movie=movieo.get(path=item.path)
                    tags=movie[0].tags
                    #print "Tags:",tags
                    if tags==u"":
                        tags=[]
                    else:
                        tags=tags.lower()
                        tags=tags.split(",")
                        tags=map(string.strip,tags)
                        
                    #print movie
                    #tags=tags.lower()
                    #print act
                    #tags=tags.split(",")
                    #print act
                    #print "Tags"
                    #print self.movie_list.indexFromItem(item).row()
                    if act=="watched":
                        ProgressBar.ProgressMessage.signal.emit("Adding %s into Watched List"%item.get_title())
                        if "watched" not in tags:
                            tags.append("watched")
                            data={"path":item.path,"tags":",".join(tags)}
                            datar=movieo.rupdate(data)
                            #print self.movie_list.indexFromItem(item).row()
                            if datar[0]:
                                self.UpdateItem.signal.emit(self.movie_list.indexFromItem(item).row(),item.path)
                    if act=="unwatched":
                        ProgressBar.ProgressMessage.signal.emit("Removing %s from Watched List"%item.get_title())
                        if "watched" in tags:
                            try:del tags[tags.index("watched")]
                            except:pass
                            data={"path":item.path,"tags":",".join(tags)}
                            datar=movieo.rupdate(data)
                            if datar[0]:
                                self.UpdateItem.signal.emit(self.movie_list.indexFromItem(item).row(),item.path)
                                
                    #ProgressBar.ProgressMessage.signal.emit(item.path)
                except:pass
                
                ProgressBar.ProgressReport.signal.emit(count)
                count=count+1
        except:pass
        #self.refresh_action()
        ProgressBar.ProgressFinished.signal.emit(True)
##########################################################################




    def method_change_cover(self,path,mid):
                try:
                    gpath=pickle.load(open("applog/moviesfoldercp.path","rb"))
                    if os.path.isfile(gpath):
                        gpath=os.path.dirname(gpath)
                except:
                    gpath=QtCore.QDir.rootPath()#.currentPath()
                    #print path
                cfile,_ = QtGui.QFileDialog.getOpenFileName(self,self.tr("Select Cover Picture"),
                                                            gpath,
                                                            self.tr("Picture Files(*.jpg *.jpeg *.gif *.png)")
                                                            )

                
                cover_path=util.cover_location(path)
                
                
                if len(cfile)!=0:
                    #print cover_path
                    has_cover=util.has_cover(path)
                    if has_cover[0]==True:
                        try:os.rename(has_cover[1],has_cover[1]+".old")
                        except:
                            try:os.remove(has_cover[1]+".old")
                            except:pass
                            try:os.rename(has_cover[1],has_cover[1]+".old")
                            except:pass
                    try:
                        shutil.copy(cfile,cover_path+cfile.split(".")[-1])
                        QtGui.QMessageBox.information(self,
                                              "Success","Cover Changed Successfully",
                                              QtGui.QMessageBox.Close,
                                              QtGui.QMessageBox.Close)
                        self.UpdateItem.signal.emit(mid,path)
                    except:
                        QtGui.QMessageBox.information(self,
                                              "Failure","Cannot change cover, change it manually",
                                              QtGui.QMessageBox.Close,
                                              QtGui.QMessageBox.Close)
                    try:
                        pickle.dump(cfile,open("applog/moviesfoldercp.path","wb"))
                    except:pass
        
     
           
    def movie_menu_signal_receivers(self):
        try:
            action=self.sender().text().lower()
            
            if action=="play":
                try:
                    path=self.movie_list.selectedItems()[0].path
                    Log(self.__name).info("Play initiating : %s",path)
                    if hasattr(immjob,"file_play"):immjob.file_play(path)
                    else:Log(self.__name).error("file_play function not found")
                except:
                    Log(self.__name).critical("Play initiation Error: %s",error())
            
            elif action=="refresh":
                self.refresh_action()
            ####################################
            elif action=="edit":
                path=self.selected_paths[0]
                meditor=MovieEditor(path)
                meditor.show()
                meditor.exec_()
            ######################################################################
            elif action=="change cover":
                self.method_change_cover(self.selected_paths[0], self.selected_ids[0])
                

            
            #######
            elif action=="rate it":
                item=self.movie_list.selectedItems()[0]
                k=RatingWindow(self,item.path)
                k.show()
                k.exec_()
            ##############################
            elif action=="open imdb":
                try:
                    imdbid=self.movie_list.selectedItems()[0].movie_data.imdbid
                    if imdbid!="":
                        webbrowser.open("http://www.imdb.com/title/%s/"%imdbid)
                    else:
                        QtGui.QMessageBox.warning(self, self.tr("Error"),self.tr("No IMDb id found\n"),QtGui.QMessageBox.Close,QtGui.QMessageBox.Close)
                except:
                    Log(self.__name).critical("Open IMDb : %s",error())
            
            elif action=="explore":
                try:
                    path=self.movie_list.selectedItems()[0].path
                    Log(self.__name).info("Explore initiating : %s",path)
                    if hasattr(immjob,"explore"):immjob.explore(os.path.dirname(path))
                    else:Log(self.__name).error("explore function not found")
                except:Log(self.__name).info("Explore initiating : %s",error())
            elif action=="update imdb id":
                #print "Update IMDb id"
                text, ok = QtGui.QInputDialog.getText(self, 'Update IMDb id', 'Enter IMDb Movie URL :')
                if ok:
                    text=text.replace(" ","")
                    if len(text)!=0:
                        imdbid=get_imdbid(text)
                        if imdbid==None:
                            QtGui.QMessageBox.warning(self, self.tr("Error"),self.tr("Invalid IMDb id\n"),QtGui.QMessageBox.Close,QtGui.QMessageBox.Close)
                        else:
                            mid=self.selected_ids[0]
                            try:
                                k=ProgressBar()
                                thr=threading.Thread(target=self.single_update_movie,args=(mid,imdbid))
                                thr.setDaemon(True)
                                k.start_progress(thr)
                                k.exec_()
                            except:pass
                            
                             
                    else:
                        QtGui.QMessageBox.warning(self, self.tr("Error"),self.tr("Invalid IMDb id\n"),QtGui.QMessageBox.Close,QtGui.QMessageBox.Close)
            ##############################            
        
            ##############################    
            elif action=="delete":#checked
                items=self.movie_list.selectedItems()
                if len(items)==1:
                    reply = QtGui.QMessageBox.question(self,
                                                   "Delete %s?"%items[0].title,
                                                   "Are you sure to delete  %s from database?"%items[0].title,
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                else:
                    reply = QtGui.QMessageBox.question(self,
                                                   "Delete %s Movies?"%len(items),
                                                   "Are you sure to delete  %s movies from database?"%len(items),
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                
                if reply == QtGui.QMessageBox.Yes:
                    Log(self.__name).info("Delete initiating For %s items",len(items))
                    try:
                        ids=self.selected_ids
                        #print ids
                        k=ProgressBar()
                        thr=threading.Thread(target=self.delete_movies,args=(ids,))
                        thr.setDaemon(True)
                        k.start_progress(thr)
                        k.exec_()
                    except Exception,e:
                        Log(self.__name).critical("%s %s",e,error())
                else:
                    Log(self.__name).info("Delete Cancelled")
            ########################
            
            
            #ELIF BLOCK#
            elif action=="favourite" or action=="unfavourite":
                #print "Showing"
                items=self.movie_list.selectedItems()
                k=ProgressBar()
                if action=="favourite":
                    thr=threading.Thread(target=self.make_favourite,args=(items,"favourite"))
                else:
                    thr=threading.Thread(target=self.make_favourite,args=(items,"unfavourite"))
                    
                thr.setDaemon(True)
                k.start_progress(thr)
                k.exec_()
            #######
            
            #Wish List Manage#
            elif action=="wish list" or action=="remove from wish list":
                #print "Showing"
                items=self.movie_list.selectedItems()
                k=ProgressBar()
                if action=="wish list":
                    thr=threading.Thread(target=self.make_wish_list,args=(items,"wish list"))
                else:
                    thr=threading.Thread(target=self.make_wish_list,args=(items,"remove from wish list"))
                    
                thr.setDaemon(True)
                k.start_progress(thr)
                k.exec_()
            #WatchList Manage#
            elif action=="watched" or action=="unwatched":
                #print "Showing"
                items=self.movie_list.selectedItems()
                k=ProgressBar()
                if action=="watched":
                    thr=threading.Thread(target=self.make_watch_list,args=(items,"watched"))
                else:
                    thr=threading.Thread(target=self.make_watch_list,args=(items,"unwatched"))
                    
                thr.setDaemon(True)
                k.start_progress(thr)
                k.exec_()
            #################################
            elif action=="add tag":
                #print "Ading Tag"
                item=self.movie_list.selectedItems()[0]
                k=TagEditor(self,item.path)
                k.show()
                k.exec_()
            elif action=="properties":
                item=self.movie_list.selectedItems()[0]
                pro=PropertiesWindow(item)
                pro.show()
                pro.exec_()
            

                
                #print "Ending With Favourite"
            
        except Exception,e:
            Log(self.__name).critical("Movie Menu Signal Receivers: %s-%s",e,error())
            
    
    


    def sort(self,sortby,order):
        for item in self.iterItems():
            item.setKey(sortby)
            if order=="asc":
                item.setAsc()
            elif order=="desc":
                item.setDesc()
                
        self.movie_list.sortItems()
        
        
    def movie_menu_selected_drive(self,drive,send_type):
        #print "Drive: ",drive
        #print "Send Type: ",send_type
        
        index=config.SEND_TO.index(send_type)
        default=True
        optiono=Option()
        try:
            copy_command=optiono.get_option("copy_command")
            if copy_command!=None and copy_command!=u"":default=False
        except:default=True
        
        paths=self.selected_paths
        if index==0:#Full Movie Folder
            if default:
                paths=[os.path.dirname(k) for k in paths]
                paths="\0".join(paths)
                #print paths
                #for path in paths:
                try:
                    thr=threading.Thread(target=immjob.send_to_default,args=(paths,drive))
                    thr.daemon=True
                    thr.start()
                except Exception,e:
                    Log(self.__name).critical("%s %s",e,error())
                    
                ##immjob.send_to_default(os.path.dirname(path),drive)
            else:
                for path in paths:
                    path=os.path.dirname(path)
                    command=copy_command.replace("%src%", path).replace("%dst%",drive)
                    commands=command.split(":-:")
                    #print commands
                    try:
                        thr=threading.Thread(target=subprocess.call,args=(commands,))
                        thr.daemon=True
                        thr.start()
                        #subprocess.call(commands)
                        time.sleep(0.1)
                    except Exception,e:
                        Log(self.__name).critical("%s %s",e,error())
                    
        elif index==1:#Only Movie File
            if default:
                paths="\0".join(paths)
                try:
                    thr=threading.Thread(target=immjob.send_to_default,args=(paths,drive))
                    thr.daemon=True
                    thr.start()
                    #immjob.send_to_default(path,drive)
                except Exception,e:Log(self.__name).critical("%s %s",e,error())
            else:
                for path in paths:
                    #path=os.path.dirname(path)
                    command=copy_command.replace("%src%", path).replace("%dst%",drive)
                    commands=command.split(":-:")
                    #print commands
                    try:
                        thr=threading.Thread(target=subprocess.call,args=(commands,))
                        thr.daemon=True
                        thr.start()
                        #subprocess.call(commands)
                        time.sleep(0.1)
                    except Exception,e:Log(self.__name).critical("%s %s",e,error())
                
        
        """            
        elif index==2:#Movie and Movie Contents
            if default:
                for path in paths:
                    cl=util.cover_location(path)
                    cl=cl[0:len(cl)-1]
                    #print cl
                    files=glob(cl+".*")
                    if len(files)!=0:dst=os.path.join(drive,util.get_name_from_path(files[0]))
                    util.make_dirs(dst)
                    for sfile in files:
                        immjob.send_to_default(sfile,dst)
            else:
                for path in paths:
                    cl=util.cover_location(path)
                    cl=cl[0:len(cl)-1]
                    #print cl
                    files=glob(cl+".*")
                    if len(files)!=0:dst=os.path.join(drive,util.get_name_from_path(files[0]))
                    util.make_dirs(dst)
                    for sfile in files:
                        command=copy_command.replace("%src%", sfile).replace("%dst%",dst)
                        commands=command.split(":-:")
                        #subprocess.call(commands)
                        #print commands
                        try:
                            thr=threading.Thread(target=subprocess.call,args=(commands,))
                            thr.daemon=True
                            thr.start()
                            time.sleep(0.3)
                        except Exception,e:Log(self.__name).critical("%s %s",e,error())
        """
        ############################
        
        
        
        
    def movie_menu_sortby(self,msg):
        #print "Sort By:",msg
        self.spin_start()
        #print self.order
        if msg=="title":
            self.sortby="title"
            self.sort(self.sortby,self.order)
        elif msg=="year":
            self.sortby="year"
            self.sort(self.sortby,self.order)
        elif msg=="imdb rating":
            self.sortby="imdbrating"
            self.sort(self.sortby,self.order)
        elif msg=="my rating":
            self.sortby="rating"
            self.sort(self.sortby,self.order)
        elif msg=="oldest":
            self.sortby="oldest"
            self.sort(self.sortby,"asc")
        elif msg=="newest":
            self.sortby="newest"
            self.sort(self.sortby,"desc")
        
        if msg=="asc":
            self.order="asc"
            self.sort(self.sortby, self.order)
        elif msg=="desc":
            self.order="desc"
            self.sort(self.sortby, self.order)
        self.spin_stop()

            #print self.movie_list.item(0)
            #print self.movie_list.itemFromIndex(0)
            #print self.movie_list.itemAt(1,10)
            #for item in self.movie_list.items(1):
            #    item.setDesc()
            #self.movie_list.sortItems()
    
    def create_context_menu(self,*kwards,**kwargs):
        selected_items=self.movie_list.selectedItems()
        size=len(selected_items)
        if size==0:
            m=MovieMenu(self.movie_list,"none")
            m.make()
            m.addMenu(self.vparent.widget_menu)
            
            m.register_all(self.movie_menu_signal_receivers)       
            m.exec_(QtGui.QCursor.pos())
        elif size==1 or size>1:
            if size==1:m=MovieMenu(self.movie_list,"single")
            elif size>1:m=MovieMenu(self.movie_list,"multiple")
            item=selected_items[0]
            tags=item.movie_data.tags
            
            #Favourite or Unfavourite
            if self.isFavourite(tags):m.show_favourite=False
            else:m.show_favourite=True
            
            ##Watched or UnWatched
            if self.isWatched(tags):m.show_watched=False
            else:m.show_watched=True
            if self.inWishList(tags):m.show_wishlist=False
            else:m.show_wishlist=True
              
            m.make()
            m.addMenu(self.vparent.widget_menu)
            m.register_all(self.movie_menu_signal_receivers)
            m.exec_(QtGui.QCursor.pos())
            
    def isFavourite(self,tags):
        tags=tags.lower()
        if tags=="":
            return False
        elif tags.find("favourite")!=-1:
            return True
        return False
    
    def isWatched(self,tags):
        tags=tags.lower()
        if tags=="":
            return False
        elif tags.find("watched")!=-1:
            return True
        return False

    def inWishList(self,tags):
        tags=tags.lower()
        if tags=="":
            return False
        elif tags.find("wish list")!=-1:
            return True
        return False
    
    def iterItems(self):
        for i in range(self.movie_list.count()):
            yield self.movie_list.item(i)    
            
        






########################
class MovieGridWidget(QtGui.QDockWidget):
    def __init__(self,menu,parent):
        super(MovieGridWidget,self).__init__("Movies",parent)
        self.setAllowedAreas(parent.areas)
        #self.thumb=Thumbnail()
        #self.setWidget(self.thumb)
        menu.addAction(self.toggleViewAction())
    def movie_by_genre(self,genre):
        self.thumb.movie_by_genre(genre)
        #self.genre_list.currentTextChanged.connect(self.genre_select)
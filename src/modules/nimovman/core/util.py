'''
Created on Jul 18, 2013

@author: KaWsEr
'''


import os
import sys
import imp
import codecs
import config
import inspect
import platform
import datetime
import urllib2
from dbmodel import Option




def next_time(tm,secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

#unicode encoder 
def encode_object(obj):
    for k,v in obj.items():
        if type(v) in (str, unicode):
            obj[k] = v.encode('utf-8')
    return obj
###################################

###get class variables
def get_vars(cls):
    return [name for name, obj in cls.__dict__.iteritems()
         if not name.startswith("_") and not inspect.isroutine(obj)]
######################################                
def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
         hasattr(sys, "importers") # old py2exe
         or imp.is_frozen("__main__")) # tools/freeze
###################



#CrossPlatform#
def getAppPath():
    dn=os.path.dirname(os.path.abspath(sys.argv[0]))
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    elif dn!="" or dn!=None:
        return dn
    else:
        aname=os.path.abspath(__file__)
        dname=os.path.dirname(aname)
    return dname
##################



#CrossPlatform#
def get_app_path():
    return getAppPath()


#CrossPlatform#
def getPlatform():
    return platform.uname()[0].lower()

#CrossPlatform#
def isWindows():
    if getPlatform()=="windows":
        return True
    return False
#####################

#CrossPlatform#
def isLinux():
    if getPlatform()=="linux":
        return True
    return False
###################

#CrossPlatform#
def isMac():
    if getPlatform()=="macosx" or getPlatform()=="darwin":
        return True
    return False
#################

##########################################
#ensure a class must be singleton#
class onlyone(object):
    def __init__(self, decorated):
        self._decorated = decorated
    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        called_string=calframe[1][4][1].replace("\n","")
        #print called_string
        try:e_str="%s must be accessed through %s.Instance()"%(called_string.split("=")[1],called_string.split("=")[1].replace("()","") ) 
        except:e_str="it must be accessed through Instance()"
        raise TypeError(e_str)
    
    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
####################################################

def get_movie_fetcher_apis(path):
    apis=[]
    if os.path.exists(path):
        apis=os.listdir(path)
        apis=map(lambda s: s.replace("."+s.split(".")[-1],""),apis)
        apis=list(set(apis))
        try:apis.remove("__init__")
        except:pass
    return apis

def get_movie_fetcher_apis_zipped(path):
    apis=[]
    if os.path.exists(path):
        remove=["__init__.py","__init__.pyc","__init__.pyo"]
        apis=os.listdir(path)
        #apis=map(lambda s: s.replace("."+s.split(".")[-1],""),apis)
        apis=list(set(apis))
        for r in remove:
            try:apis.remove(r)
            except:pass
    return apis

def get_plugins(path):
    apis=[]
    if os.path.exists(path):
        apis=os.listdir(path)
        apis=map(lambda s: s.replace("."+s.split(".")[-1],""),apis)
        apis=list(set(apis))
        try:apis.remove("__init__")
        except:pass
    return apis

#####################################################
def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
########################

# # #######################################################
def form_dict(path):
    """This Will Form the dictionary From the text data"""
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
                    kin=line_data[0].strip().decode("utf-8")
                    data[kin.lower()]=line_data[2].strip()
                except:pass
    return data
# # # # # # # # # # #  # # #################

def get_name_from_path(path):
    if path.find("/")!=-1:path=path.split("/")[-1]
    elif path.find("\\")!=-1:path= path.split("\\")[-1]
    path=path.replace("."+path.split(".")[-1],"")
    return path

def get_filename_from_path(path):
    if path.find("/")!=-1:path=path.split("/")[-1]
    elif path.find("\\")!=-1:path= path.split("\\")[-1]
    #path=path.replace("."+path.split(".")[-1],"")
    return path


##################################

# # # #
def find_cover_data_path():
    opt=Option()
    try:data_dir=opt.get_option("data_dir")
    except Exception:return (None,None)
    try:cover_dir=Option().get_option("cover_dir")
    except:return (None,None)
        
    try:data_dir_index=config.DATA_DIR.index(data_dir)
    except Exception:data_dir_index=0
    try:cover_dir_index=config.DATA_DIR.index(cover_dir)
    except:cover_dir_index=0
        
        #print data_dir_index,cover_dir_index
    data_path=None
    if data_dir_index==1:data_path=config.C_DATA_PATH     
    elif data_dir_index==2:
        try:data_path=Option().get_option("data_dir_custom")
        except:return (None,None)
            
    cover_path=None
    if cover_dir_index==1:
        cover_path=config.C_COVER_PATH
    elif cover_dir_index==2:
        try:cover_path=opt.get_option("cover_dir_custom")
        except:return (None,None)
    return (data_path,cover_path)
# # # # # # # # # # # # # # # # # # # # # # #


def make_dirs(p):
    if os.path.isfile(p):dn=os.path.dirname(p)
    else:dn=p
    if dn!="":
        if not os.path.exists(dn):os.makedirs(dn)
    if os.path.exists(dn):return True
    return False
# # # # # # # # # # # # # # # # # # # # # # #


def name_without_ext(name):return name.replace("."+name.split(".")[-1],"")
# # # #  # #  # # # #  # ##   #   #  #


def make_data(data,save_as):
        """This Will Create The Text Data"""
        #Log(self.__name).info("Making Data: %s",save_as)
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
            except Exception:return False
        return False
# # # # # # # # # # #  # # # # # # # #  # # # # # #     ##  # # # # #  # # # # #  # # # #  # #  # #  # #  #

def make_unique_dict(data):
    ndata={}
    for i in data.keys(): ndata[i.lower()]=data[i]
    return ndata
#####################################################

def download_file(url,save_as):
        """Download Any File"""
        f = urllib2.urlopen(url)
        with open(save_as,'wb') as output:
            while True:
                buf = f.read(65536)
                if not buf:break
                output.write(buf)
        return True
####################################################
def cover_location(path):
    #print icover_path
    name=os.path.basename(path).replace(path.split(".")[-1],"")
    _,cover_path=find_cover_data_path()
    if cover_path!=None:icover_path=os.path.join(cover_path,name)
    else:icover_path=path.replace(path.split(".")[-1],"")
    return icover_path
# # # # # # # # #  # #  #############################


def has_cover(path):
        option=Option()
        try:cover_format=option.get_option("C_COVER_FORMAT")
        except:cover_format=config.C_COVER_FORMAT
        
        #print icover_path
        name=os.path.basename(path).replace(path.split(".")[-1],"")
        _,cover_path=find_cover_data_path()
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
##########################################################

    

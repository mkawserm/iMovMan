'''
Created on Jul 18, 2013

@author: KaWsEr
'''

import os
import sys
import util
import codecs
import datetime

##### Cover Configuration ########
COVER_WIDTH=214
COVER_HEIGHT=317
##################################






###### Internal Configuration #####
## Extension ##
EXT_DB=".cimd"
EXT_THEME=".cimt"
EXT_PLUGIN=".cimp"
EXT_PDB=".cipd"
EXT_TXT=".ctxt"
EXT_UPDATE_FILE=".ciuf"
###################################
MOVIE_DB_KEYS=["Title",
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
ALLOWED_IN_TITLE=["title","imdbrating","genre","year","runtime","rated","imdbvotes"]

MOVIE_DB_KEYS_EXTRA=["movie_id",
                     "path",
                     "tags",
                     "cdate",
                     "udate",
                     "visibility",
                     "rating"]
####################################

DATA_DIR=["Movie Directory",
          "Application Directory",
          "Custom Directory"]
EN_DIS=["Enabled","Disabled"]

SEND_TO=["Full Movie Folder","Only Movie File","Pop up settings when send To initiated"]
###Deleted "Movie and Movie contents"


APP_NAME="iMovMan"
APP_DEVELOPER="KaWsEr"
APP_DEVELOPER_INFO="SubsCribe at http://www.cliodin.com"
APP_VERSION="1.3.0.0"
#APP_CODENAME="Super User Preview"
APP_WEB="http://bit.ly/14g1cQl"
APP_WEB_LABEL="cliodin.com"
APP_DESCRIPTION="""iMovMan means Instant Movie Manager which manage all movies of your hard drive with movie cover and IMDb information such as rating, genre, actors, directors etc. It'll help a user to search and manage movies efficiently."""
APP_CREDITS="""Credits:<br/> 
 &nbsp;<a href="http://on.fb.me/11XcIOH">Khusbo Rezwan</a> :: Icon Design<br/>""" 
next_year=int(datetime.date.today().strftime("%Y"))+1
APP_COPYRIGHT="copyright (c) 2013-"+str(next_year)+" cliodin.com"
APP_HELP="http://on.fb.me/19zg0wM"
APP_FB="http://on.fb.me/133Euy8"

APP_UPDATE_CHECK="http://bit.ly/16DiWqR"#it is used to check if a new version is available or not

LOG_FILE=os.path.realpath(os.path.join(util.get_app_path(),"applog/iMovMan.log"))

C_DATA_DIR=os.path.realpath(os.path.join(util.get_app_path(),"data"))
C_COVER_PATH=os.path.realpath(os.path.join(util.get_app_path(),"data/data-cover"))
C_DATA_PATH=os.path.realpath(os.path.join(util.get_app_path(),"data/data-cover"))

#C_ACTIVE_THEME=
BUILD_FILE="data/zimmlib/zbuild/build-prop.idat"
C_THEME_PATH="data/zimmlib/web-ui/themes"
C_APPICON_PATH="data/zimmlib/appicon"
C_APPANIM_PATH="data/zimmlib/appanim"
C_APPSPLASH_PATH="data/zimmlib/appsplash"
C_ASSETS_PATH="data/zimmlib/assets"
C_MOVIE_FORMAT=["mp4","mkv","avi","flv","vob","mov","mpg","wmv","m4v"]
C_COVER_FORMAT=["jpg","gif","png","jpeg","bmp"]
C_DEFAULT_THEME="default"

C_MODULE_PATH=os.path.realpath(os.path.join(util.get_app_path(),"data/zimmlib/modules"))
C_DLL_PATH=os.path.realpath(os.path.join(util.get_app_path(),"data/zimmlib/dlls"))
C_PLUGIN_PATH=os.path.realpath(os.path.join(util.get_app_path(),"data/zimmlib/modules/plugins"))
C_USER_PLUGIN_PATH=os.path.realpath(os.path.join(util.get_app_path(),"data/plugins"))

#C_MOVIE_FETCHER_API_PATH=os.path.realpath(os.path.join(util.get_app_path(),"data/ziimlib/modules/mapis"))


if not os.path.exists(C_PLUGIN_PATH):
    C_PLUGIN_PATH="modules/plugins"

C_DEFAULT_API="omdbapi" ##Access Via #movie_api#
C_MAPI_PATH=os.path.realpath(os.path.join(util.get_app_path(),"data/zimmlib/mapis"))


#print C_MAPI_PATH
##### Database Configuration #####
MAX_CONNECTION=3#maximum connection of db


DB_USER=os.path.realpath(os.path.join(C_DATA_DIR,"db/db_user"+EXT_DB))

DB_MOVIE=os.path.realpath(os.path.join(C_DATA_DIR,"db/db_movies"+EXT_DB))
DB_MOVIE_META=os.path.realpath(os.path.join(C_DATA_DIR,"db/db_movie_meta"+EXT_DB))
DB_POSTER=os.path.realpath(os.path.join(C_DATA_DIR,"db/db_poster"+EXT_DB))

DB_OPTION=os.path.realpath(os.path.join(C_DATA_DIR,"db/db_option"+EXT_DB))
DB_TRASH=os.path.realpath(os.path.join(C_DATA_DIR,"db/db_trash"+EXT_DB))

DB_STATUS=os.path.realpath(os.path.join(C_DATA_DIR,"zimmlib/status"+EXT_DB))

###################################

sys.path.append(C_MODULE_PATH)
sys.path.append(C_DLL_PATH)
sys.path.append(C_PLUGIN_PATH)
sys.path.append(C_USER_PLUGIN_PATH)
sys.path.append(C_MAPI_PATH)





def appsplash(name):
    ipath=os.path.join(C_APPSPLASH_PATH,name+".png")
    if os.path.exists(ipath):return ipath
    else:return None
##################################################
def appicon(name):
    ipath=os.path.join(C_APPICON_PATH,name+".png")
    if os.path.exists(ipath):return ipath
    else:return None
##################################################    
def appanim(name):
    ipath=os.path.join(C_APPANIM_PATH,name+".gif")
    if os.path.exists(ipath):return ipath
    else:return None
##################################################    
def asset(name):
    ipath=os.path.join(C_ASSETS_PATH,name)
    if os.path.exists(ipath):return ipath
    else:return None
##################################################
def config_parser(path):
    """This Will Form the dictionary From the text data"""
    data={}
    try:
        f=codecs.open(path, "r", "utf-8")
        text=f.read()
        f.close()
    except Exception:text=None
    if text!=None:
        lines=text.split("\n")
        for sline in lines:
            if sline!="" or sline==None:line_data=sline.partition(":")
            if len(line_data)==3:
                try:
                    kin=line_data[0].strip().decode("utf-8")
                    #data[kin]=line_data[2].strip()
                    data[kin.lower()]=line_data[2].strip()
                except:pass
    else:return {}
    
    return data
##################################################
def is_usable(uv):
    cu=APP_VERSION
    cu=cu.split(".")
    uv=uv.split(".")
    for i in range(0,4):
        try:cu[i]=int(cu[i])
        except:return False
        try:uv[i]=int(uv[i])
        except:return False
        
    if len(cu)==len(uv)==4:
        #print cu==uv,"cu=uv"
        #print cu>=uv,"cu>=uv"
        #print cu<uv,"cu<uv"
        #print cu!=uv,"cu!=uv"
        if cu>=uv:return True
    return False

def is_new(uv):
    cu=APP_VERSION
    cu=cu.split(".")
    uv=uv.split(".")
    for i in range(0,4):
        try:cu[i]=int(cu[i])
        except:return False
        try:uv[i]=int(uv[i])
        except:return False
        
    if len(cu)==len(uv)==4:
        #print cu==uv,"cu=uv"
        #print cu>=uv,"cu>=uv"
        #print cu<uv,"cu<uv"
        #print cu!=uv,"cu!=uv"
        if cu<uv:return True
    return False
###############################################
'''
Created on Jun 14, 2013

@author: KaWsEr
'''
import os
import sys
import utility
import datetime

APP_NAME="iMovMan"
APP_DEVELOPER="KaWsEr"
APP_DEVELOPER_INFO="SubsCribe at http://www.cliodin.com"
APP_VERSION="1.0.0.0"
APP_CODENAME="beta one"
APP_WEB="http://bit.ly/14g1cQl"
APP_WEB_LABEL="cliodin.com"
APP_DESCRIPTION="""iMovMan means Instant Movie Manager which
 manage all movies of your hard drive with movie cover and 
 imdb information such as rating,genre,actors,directors etc.It'll help a user to search and manage movies efficiently"""
 
next_year=int(datetime.date.today().strftime("%Y"))+1
APP_COPYRIGHT="(c) 2013-"+str(next_year)+" cliodin.com"



APP_UPDATE_CHECK="http://bit.ly/16DiWqR"#it is used to check if a new version is available or not


C_DATA_DIR=os.path.realpath(os.path.join(utility.get_app_path(),"data"))
#C_ACTIVE_THEME=
C_THEME_PATH="data/web-ui/themes"
C_APPICON_PATH="data/appicon"
C_APPANIM_PATH="data/appanim"
C_APPSPLASH_PATH="data/appsplash"
C_ASSETS_PATH="data/assets"
C_MOVIE_FORMAT=["mp4","mkv","avi","flv","vob","mov","mpg","wmv","m4v"]
C_COVER_FORMAT=["jpg","gif","png","jpeg","bmp"]
C_DEFAULT_THEME="default"
C_MODULE_PATH=os.path.realpath(os.path.join(utility.get_app_path(),"data/ziimlib/modules"))
C_DLL_PATH=os.path.realpath(os.path.join(utility.get_app_path(),"data/ziimlib/dlls"))


sys.path.append(C_MODULE_PATH)
sys.path.append(C_DLL_PATH)



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
    ipath=os.path.join(C_ASSETS_PATH,name+".png")
    if os.path.exists(ipath):return ipath
    else:return None
##################################################
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from glob import glob
import py2exe
from distutils.core import setup
import datetime
import codecs
import zipfile


DATA_DIR="data/"
LIB_DIR=DATA_DIR+"zimmlib/"
BUILD_DIR=LIB_DIR+"zbuild/"
BUILD_FILE=BUILD_DIR+"build-prop.idat"

def make_dirs(p):
    if os.path.isfile(p):dn=os.path.dirname(p)
    else:dn=p
    if dn!="":
        if not os.path.exists(dn):os.makedirs(dn)
    if os.path.exists(dn):return True
    return False
# # # # # # # # # # # # # # # # # # # # # # #

def read_in_chunks(file_object, chunk_size=4096):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def form_dict(path):
    """This Will Form the dictionary From the text data"""
    data={}
    try:
        f=codecs.open(path, "r", "utf-8")
        text=f.read()
        f.close()
        #print text
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





def build_prop():
    t=raw_input("Enter Build Type: 1=Beta,2=Stable :")
    try:t=int(t)
    except:t=1
    
    if t==1:btype="Beta"
    elif t==2:btype="Stable"
    
    
    data={}
    bnumber=0
    if os.path.exists(BUILD_FILE):
        data=form_dict(BUILD_FILE)
    if data.has_key("buildnumber"):bnumber=data["buildnumber"]
    try:bnumber=int(bnumber)+1
    except:bnumber=1
    
    st_time=datetime.datetime.now()
    string_time="%s:%s:%s-%s:%s:%s"%(st_time.day,st_time.month,st_time.year,st_time.hour,st_time.minute,st_time.second)
    name=raw_input("Enter Build Name:")
    try:name=str(name)
    except:name="unspecified"
    
    changelog=open("changelog.txt","r")
    clog=""
    for i in read_in_chunks(changelog):
        clog=clog+i
    clog=clog.replace("\n","")
    changelog.close()
    make_dirs(BUILD_DIR)
    f=open(BUILD_FILE,"w+")
    f.write("BuildName: %s"%name)
    f.write("\nBuildType: %s"%btype)
    f.write("\nBuildString: %s"%string_time)
    f.write("\nBuildNumber: %s"%bnumber)
    f.write("\nChangeLog: %s"%clog)
    f.close()
#########################
build_prop()



print
print
print







sys.path.append("E:\WorkSpace\EclipseWorkspace\iMovMan\Dependency\Microsoft.VC90.CRT")
sys.argv.append("py2exe")

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("msvcr90.dll","MSVCP90.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

data_files1 = [("Microsoft.VC90.CRT", glob(r'E:\WorkSpace\EclipseWorkspace\iMovMan\Dependency\Microsoft.VC90.CRT\*.*'))]
data_files2=[("imageformats",glob( r"C:\Python27\Lib\site-packages\PySide\plugins\imageformats\*.*"  ) )]
#"dll_excludes":['shiboken-python2.7.dll','QtCore4.dll','QtGui4.dll'],


def FormDataFiles():
    dir_list=["data/"]
    data_files=[]
    for i in dir_list:
        for (apath, dirs, files) in os.walk(i):
            for s_file in files:
                file_path=os.path.join(apath, s_file)
                dir_path=os.path.dirname(file_path)
                data_files.append((dir_path,[file_path]))
    return data_files

 

data_files=FormDataFiles()
for i in data_files1:
    data_files.append(i)
    
for i2 in data_files2:
    data_files.append(i2)

#data_files = [('data/ui', ['data/ui/iMovMan1.glade']),('data', ['data/iMovMan.png'])]
"""
         {
         'script': 'updater.py',
         'icon_resources': [(0, "ico/imovman.ico")] ,
         'dest_base': 'iMovMan-updater'
          }
"""


windows=[
         {
          'script': 'iMovMan.py',
          'icon_resources': [(0, "ico/exe.ico")] ,
          'dest_base': 'iMovMan'
          },
         
         {
          'script': 'updater.py',
          'icon_resources': [(0, "ico/exe.ico")] ,
          'dest_base': 'iMovMan-updater'
          },

         
         ]




opt={'py2exe': dict(includes=[
                              'psutil',
                              #'bottle',
                              #'cherrypy',
                              'sqlalchemy',
                              #'pylzma',
                              #'win32file',
                              #'win32com',
                              #'webapp2',
                              #'webob',
                              #'PySide.QtNetwork'
                              ],
					excludes=[
                              "tcl",
                              #"PySide"
                              ],
                    
                    packages=['modules',
                              #'modules.mapis',
                              #'modules.plugins',
                              'sqlalchemy',
                              ],
                    dll_excludes= [
                                   #"QtGui4.dll",
                                   #"shiboken-python2.7.dll",
                                   #"QtCore4.dll",
                                   #"pyside-python2.7.dll",
                                   #"POWRPROF.dll",
                                   "API-MS-Win-Core-LocalRegistry-L1-1-0.dll",
                                   "tcl85.dll",
                                   "tk85.dll","tcl",
                                   "sMSVCP90.dll",
                                   "HID.DLL",
                                   "w9xpopen.exe",
                                   "API-MS-Win-*"],
                    optimize=2,
                    bundle_files=3,#3
					compressed=False,#Flase
					skip_archive=True#True
					)}#2 default i useds

#"""



"""

    3 (default) don't bundle
    2 bundle everything but the Python interpreter
    1 bundle everything, including the Python interpreter

	
""" 
if 'py2exe' in sys.argv:
    
 
    kwargs = dict(#console=['imovman-start.py'],
                  windows=windows,
                  zipfile="data/zimmlib/modules.zip",
                  #zipfile=None,
                  options=opt,
                  data_files=data_files)
else:
    kwargs = dict(scripts=['imovman-start.py'])




##############################
setup(name='iMovMan',
      version='1.1.0.0',
	  description='Instant Movie Manager',
      author='KaWsEr',
	  #copyright='(c) 2013-2014 cliodin.com',
      author_email='mkawserm@facebook.com',
      #packages=['imovman','sqlalchemy'],
      package_data={'imovman': ['data/*']},
      **kwargs)

########################


rem_list1=glob(r'dist\\data\\zimmlib\API-MS*.*')
for i in rem_list1:os.remove(i)
rem_list2=glob(r'dist\\data\\zimmlib\tcl*.*')
for i in rem_list2:os.remove(i)



def ciuf(src, dst,mode="w"):
    zf = zipfile.ZipFile("%s.ciuf" % (dst), mode)
    abs_src = os.path.abspath(src)
    #print abs_src
    for dirname, subdirs, files in os.walk(src):
        #break
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            arcname = src+"\\"+arcname
            #print 'zipping %s as %s' % (os.path.join(dirname, filename),arcname)
            zf.write(absname, arcname)
    zf.close()









def create_update_file():
    MAPIS="data\\zimmlib\\mapis"
    MODULES="data\\zimmlib\\modules"
    
    
    APPANIM="data\\zimmlib\\appanim"
    APPICON="data\\zimmlib\\appicon"
    ASSETS="data\\zimmlib\\assets"
    ZBUILD="data\\zimmlib\\zbuild"
    #print os.path.exists(MAPIS)
    #print os.path.exists(APPANIM)
    data=form_dict(BUILD_FILE)
    #print data
    name=data["buildnumber"]+"_"+data["buildname"].replace(" ","-")+"_"+data["buildstring"].replace(":","").replace("-","_")
    os.chdir("dist")
    ciuf(MAPIS,name)
    ciuf(MODULES,name,"a")
    ciuf(APPANIM,name,"a")
    ciuf(APPICON,name,"a")
    ciuf(ASSETS,name,"a")
    ciuf(ZBUILD,name,"a")




create_update_file()



"""
for i in range(100):
    k=raw_input("Enter q key to exit")
    if k=="q":break
"""
    
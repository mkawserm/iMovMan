#!/usr/bin/env python

"""
ModuleName: utility
Version: 1.0.0
Coder: KaWsEr
HomePage: https://facebook.com/mkawserm

Python Utility Module which contains 
some necessary functions to solve task easily
"""

"""

Available Functions:
 
 1.getAppPath() -> returns the application path
 2.get_app_path() ->same as getAppPath()
 

"""



import os
import re
import sys
import imp
import string
import inspect
import platform
import datetime
import urllib2
#import subprocess




#uicode ecoder 
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



#only windows#
def getDrives():
    drives = []
    if isWindows():
        from ctypes import windll
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.uppercase:
            if bitmask & 1:
                #print bitmask & 1
                if letter.lower()!="c":
                    drives.append(os.path.realpath(letter+":"))
            bitmask >>= 1
    elif isLinux():
        root="/media"
        dirs=os.listdir(root)
        for idr in dirs:
            drives.append(os.path.realpath(os.path.join(root,idr+"/")))
    return drives



def get_drives():return getDrives()

def open_folder(dst):
    dst=unicode(dst)
    #print dst
    if isWindows():
        #print dst
        import win32api
        win32api.ShellExecute(None, 'open', 'explorer.exe',
                      '/n,"%s"'%dst, None, 1)
        #subprocess.Popen('explorer r"%s"'%(dst))
  

def get_drive_details():
 my_drives=[]
 
 if isWindows():
  import win32api
  drives = win32api.GetLogicalDriveStrings()
  drives = drives.split('\000')[:-1]
  try:
   for dr in drives:
    dr=unicode(dr)
    #print dr
    try:
     my_drives.append([dr,win32api.GetVolumeInformation(dr)[0]])
    except:
     pass
  except  Exception,e:
   print e
  return my_drives
 return None


#make parent dirs
def make_dirs(u_db):
    if u_db!=None:
        if not os.path.exists(os.path.dirname(u_db)):
            os.makedirs(os.path.dirname(u_db))
###############################

#to get all database tables of the db
def get_tables(object):
 rdata=[]
 try:
  eng=object.getEngine()
  c=eng.connect()
  cur=c.execute('SELECT name FROM sqlite_master WHERE type = "table"')
  data = cur.fetchall()
  #print data
  for i in data:
   rdata.append(i[0])
 except Exception,e:
  #print e
  return []
 return rdata

def getCover(url,save_as):
 file = urllib2.urlopen(url)
 with open(save_as,'wb') as output:
  while True:
   buf = file.read(65536)
   if not buf:
    break
   output.write(buf)

#all os
def file_open(fpath):
 #print fpath
 os.startfile(fpath)

def default_file_open(fpath):
 #print fpath
 os.startfile(unicode(fpath))

 

def default_file_copy(src,dst):
 if isWindows():
  from shell import shell, shellcon
  Logger().debug(src)
  shell.SHFileOperation ((0, shellcon.FO_COPY, unicode(src),unicode(dst), 0, None, None))
  Logger().debug(dst)

def get_smart_name(name):
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
    if title!=None:
     title=title.replace("."," ").strip()
    return title,year 
  except Exception,e:
   print e
   return title,year
  return title,year


#Logger Class To Log Info#
class Logger(object):
 
 @staticmethod
 def debug(arg_text,**kwargs):
  Logger.log("debug",arg_text,**kwargs)
 
 @staticmethod
 def error(arg_text,**kwargs):
  Logger.log("error",arg_text,**kwargs)
 
 @staticmethod
 def warning(arg_text,**kwargs):
  Logger.log("warning",arg_text,**kwargs)
 
 @staticmethod
 def info(arg_text,**kwargs):
  Logger.log("info",arg_text,**kwargs)
 
 @staticmethod
 def log(arg_type,arg_text,**kwargs):
  if arg_type=="debug":
   main_fpath="debug.log"
   fpath="debug.log"
  elif arg_type=="error":
   main_fpath="error.log"
   fpath="error.log"
  elif arg_type=="warning":
   main_fpath="warning.log"
   fpath="warning.log"
  elif arg_type=="txt":
   main_fpath="TxT.txt"
   fpath="TxT.txt"
  else:
   main_fpath="info.log"
   fpath="info.log"
  
  
  arg_mode="a+"
  if kwargs.has_key("mode"):
   arg_mode=kwargs["mode"]
   if arg_mode=="r":
    arg_mode="w+"
   if arg_mode=="r+":
    arg_mode="w+"
   elif arg_mode=="w":
    arg_mode="w+"
   elif arg_mode=="a":
    arg_mode="a+"
   else:
    arg_mode="a+"
  if kwargs.has_key("fpath"):
   fpath=os.path.join(kwargs["fpath"],fpath)
  if kwargs.has_key("fname"):
   fpath=kwargs["fname"]
  try:
   f=open(fpath,arg_mode)
  except Exception,e:
   try:
    f=open(main_fpath,arg_mode)
   except Exception,e:
    print e
  try:
   f.write(str(datetime.datetime.now())+" - "+arg_text+"\n")
   f.close()
  except Exception,e:
   print e
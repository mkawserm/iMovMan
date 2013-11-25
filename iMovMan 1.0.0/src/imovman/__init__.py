#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SoftwareName: iMovMan
SoftwareVersion: 1.0.0
SoftwareDeveloper: KaWsEr
SoftwareHomePage: http://on.fb.me/XTyTXv
DeveloperFacebookProfile: http://on.fb.me/133fXtA
"""
"""
iMovMan means Instant Movie Manager which manage
all local movies of hard drive with cover and imdb info
such as rating,genre,actors,directors etc 
"""



import os
import ast
import sys
import json
import time
import operator
import threading
import webbrowser




import idb
import config
import crawler
import utility




from browser import uWindow
from webui import CherryPyServer
from idb import getAppDetails,icon



































        
  
def setup_db():
    cdb=idb.CDb()
    if not cdb.has_key("setup"):
        cdb.set_default()
    #lst=[os.path.realpath("F:\\MoviesWorld\\Satil")]
    #cdb.add("movie_path",lst)
    #cdb.add("movie_format",["flv","mkv","mp4","m4v","avi"])
    #print cdb.all()






"""Application Starting Point"""
def main():
    print "Main Program Started"
    #print has_update()
    server=CherryPyServer()
    server.prun()
    #Run this to make custom iconset to stock
    win=uWindow(server.site_name)
    win.start()
    #app=threading.Thread(target=win.start)
    #app.daemon=True
    #app.start()
    import kill
    
    




###############################








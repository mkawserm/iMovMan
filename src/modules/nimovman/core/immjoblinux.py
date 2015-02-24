'''
Created on Aug 13, 2013

@author: KaWsEr
'''
import os
import subprocess
from PySide import QtCore


def startfile(filename):
    try:
        os.startfile(filename)
    except:
        subprocess.Popen(['xdg-open', filename])


def file_play(fpath):
    #print fpath
    startfile(unicode(fpath))


def get_drive_details():
    drives=[]
    
    for drive in QtCore.QDir.drives():
        drives.append([drive.absolutePath(),""])
        print dir(drive)
        #break
    return drives
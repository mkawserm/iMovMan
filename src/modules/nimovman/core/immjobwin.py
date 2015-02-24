'''
Created on Aug 13, 2013

@author: KaWsEr
'''

import os
import string
try:
    win32api=__import__("win32api")
    exec("from shell import shell, shellcon")
except:pass
exec("from ctypes import windll")




#print dir(win32api)
def get_drives():
    drives = []
    bitmask=None
    exec("bitmask = windll.kernel32.GetLogicalDrives()")
    for letter in string.uppercase:
        if bitmask & 1:
            #print bitmask & 1
            #if letter.lower()!="c":
            drives.append(os.path.realpath(letter+":"))
        bitmask >>= 1
    return drives


def get_drives_details():
    my_drives=[]
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    try:
        for dr in drives:
            dr=unicode(dr)
            #print dr
            try:my_drives.append([dr,win32api.GetVolumeInformation(dr)[0]])
            except:pass
    except  Exception,e:
        print e
    return my_drives


def file_play(fpath):
    #print fpath
    os.startfile(unicode(fpath))
    
def explore(dst):
    dst=unicode(dst)
    #win32api.ShellExecute(None, 'open', 'explorer.exe','/n,"%s"'%dst, None, 1)
    os.startfile(dst)

def send_to_default(src,dst):
    exec("shell.SHFileOperation ((0, shellcon.FO_COPY, unicode(src),unicode(dst), 0, None, None))")
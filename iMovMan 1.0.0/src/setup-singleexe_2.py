#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from glob import glob
import py2exe
from distutils.core import setup
sys.path.append("G:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")


origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("msvcr90.dll","MSVCP90.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

data_files1 = [("Microsoft.VC90.CRT", glob(r'G:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
data_files2=[("imageformats",glob( r"C:\Python27\Lib\site-packages\PySide\plugins\imageformats\*.*"  ) )]



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
    data_files.append(i)\
    
for i2 in data_files2:
    data_files.append(i2)

#data_files = [('data/ui', ['data/ui/iMovMan1.glade']),('data', ['data/iMovMan.png'])]
windows=[{'script': '__main__.py',
          'icon_resources': [(0, "data/ico/imovman.ico")] ,
          'dest_base': 'iMovMan'}]

opt={'py2exe': dict(includes=[
                              'bottle',
                              'cherrypy',
                              'sqlalchemy',
                              #'webapp2',
                              #'webob',
                              'PySide.QtNetwork'],
					excludes=["tcl"],
                    
                    packages=['imovman',
                              'sqlalchemy',
                              ],
                    dll_excludes= ["API-MS-Win-Core-LocalRegistry-L1-1-0.dll","tcl85.dll","tk85.dll","tcl","sMSVCP90.dll", "HID.DLL", "w9xpopen.exe","API-MS-Win-*"],
                    optimize=2,
                    bundle_files=3,#3
					compressed=False,
					skip_archive=True
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
                  zipfile="data/zimmlib/modules/modules.zip",
                  options=opt,
                  data_files=data_files)
else:
    kwargs = dict(scripts=['imovman-start.py'])



setup(name='iMovMan',
      version='1.0.0.0',
	  description='Instant Movie Manager',
      author='KaWsEr',
	  #copyright='(c) 2013-2014 cliodin.com',
      author_email='mkawserm@facebook.com',
      #packages=['imovman','sqlalchemy'],
      package_data={'imovman': ['data/*']},
      **kwargs)



#"""
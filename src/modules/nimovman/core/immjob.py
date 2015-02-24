'''
Created on Aug 13, 2013

@author: KaWsEr
'''


import util
if util.isLinux():from immjoblinux import *
elif util.isWindows():from immjobwin import *
elif util.isMac():from immjobmac import *
'''
Created on May 24, 2013

@author: KaWsEr
'''
import os
import util





"""
This Module is used to kill the app
"""
def do():
    if util.isWindows():
        import ctypes
        PROCESS_TERMINATE = 1
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, os.getpid())
        ctypes.windll.kernel32.TerminateProcess(handle, -1)
        ctypes.windll.kernel32.CloseHandle(handle)
    else:
        import signal
        os.kill(os.getpid(), signal.SIGALRM)
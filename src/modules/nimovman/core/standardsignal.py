'''
Created on Aug 15, 2013

@author: KaWsEr
'''
from PySide import QtCore



class Signal(QtCore.QObject):
    signal=QtCore.Signal()
class SignalBool(QtCore.QObject):
    signal=QtCore.Signal(bool)
class SignalInt(QtCore.QObject):
    signal=QtCore.Signal(int)
class SignalUnicode(QtCore.QObject):
    signal=QtCore.Signal(unicode)
class SignalString(QtCore.QObject):
    signal=QtCore.Signal(str)
class MessageSendU(QtCore.QObject):
    signal=QtCore.Signal(unicode,unicode)
class MessageSend(QtCore.QObject):
    signal=QtCore.Signal(str,str)

class IntUnicode(QtCore.QObject):
    signal=QtCore.Signal(int,unicode)
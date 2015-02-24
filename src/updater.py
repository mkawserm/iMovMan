'''
Created on Aug 25, 2013

@author: KaWsEr
'''
import os
import sys
import imp
import shutil
import codecs
import platform
import zipfile
from PySide import QtGui
from PySide import QtCore
EXT_UPDATE_FILE=".ciuf"                                                                                                                                                                                                                                            "};"""

import threading
#import time
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

class Signal(QtCore.QObject):
    signal=QtCore.Signal()
class SignalInt(QtCore.QObject):
    signal=QtCore.Signal(int)
class SignalBool(QtCore.QObject):
    signal=QtCore.Signal(bool)
class SignalUnicode(QtCore.QObject):
    signal=QtCore.Signal(unicode)


class ProgressBar(QtGui.QDialog):
    ProgressStarted=SignalInt()
    ProgressReport=SignalInt()
    ProgressFinished=SignalBool()
    ProgressMessage=SignalUnicode()
    def __init__(self):
        super(ProgressBar,self).__init__(None)
        self.icon=QtGui.QIcon(os.path.join(getAppPath(),"data/updater/immupdater.png"))
        self.setWindowIcon(self.icon)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint )
        self.setModal(True)
        
        self.progress_bar=QtGui.QProgressBar(self)
        self.progress_bar.setFixedWidth(400)
        self.progress_bar.setMinimum(0)
        self.setFixedWidth(400)
        self.setFixedHeight(50)
        #TrashWindow.TotalTrashItems.signal.connect(self.total_trash_items)
        #TrashWindow.TotalTrashed.signal.connect(self.trashed)
        #TrashWindow.TrashingFinished.signal.connect(self.finished)
        self.ProgressStarted.signal.connect(self.started)
        self.ProgressReport.signal.connect(self.progress_report)
        self.ProgressFinished.signal.connect(self.finished)
        self.ProgressMessage.signal.connect(self.progress_message)
        self.show()
    
    def progress_message(self,msg):
        self.setWindowTitle(msg)
    def started(self,number):
        self.total=number
        self.progress_bar.setMaximum(number)
    def start_progress(self,thr):
        self.thr=thr
        self.thr.start()
        #self.thr()
        
    def progress_report(self,number):
        #percentage=(number*100.0)/self.total
        self.progress_bar.setValue(number)
        #self.setWindowTitle("%s "%percentage+"%")
        if number==self.total:
            self.close()
    def keyPressEvent(self,event):pass    
    def finished(self,b):
        self.thr.join()
        self.close()


#########################










    
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

def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
         hasattr(sys, "importers") # old py2exe
         or imp.is_frozen("__main__")) # tools/freeze
###################

def get_imovman_pid():
    import psutil
    process = filter(lambda p:p.name == "iMovMan" or p.name == "imovman" or p.name == "iMovMan.exe", psutil.process_iter())
    for i in process:return i.pid
    return False



#CrossPlatform#
def getPlatform():return platform.uname()[0].lower()
#CrossPlatform#
def isWindows():
    if getPlatform()=="windows":return True
    return False
#####################

#CrossPlatform#
def isLinux():
    if getPlatform()=="linux":return True
    return False
###################
#CrossPlatform#
def isMac():
    if getPlatform()=="macosx" or getPlatform()=="darwin":return True
    return False
#################
#CrossPlatform#
def getAppPath():
    dn=os.path.dirname(os.path.abspath(sys.argv[0]))
    if main_is_frozen():return os.path.dirname(sys.executable)
    elif dn!="" or dn!=None:return dn
    else:dname=os.path.dirname(os.path.abspath(__file__))
    return dname
#CrossPlatform#
def get_app_path():return getAppPath()
###################################################







class UpdaterWindow(QtGui.QMainWindow):
    CorruptSignal=Signal()
    SuccessSignal=Signal()
    def __init__(self):
        super(UpdaterWindow,self).__init__(None)
        self.setWindowTitle("iMovMan Updater")
        self.setFixedSize(500,520)
        self.icon=QtGui.QIcon(os.path.join(getAppPath(),"data/updater/immupdater.png"))
        self.setWindowIcon(self.icon)
        self.version_list=[]
        
        self.DIR="data/updatelog"

        make_dirs(self.DIR)
        
        self.selected_item=None

        

        self.version_list_widget = QtGui.QListView(self)
        self.version_list_widget.move(0,20)
        #self.version_list_widget.set
        self.version_list_widget.setMinimumSize(200,500)
        self.version_list_model = QtGui.QStringListModel(self.version_list_widget)
        self.version_list_model.setStringList(self.version_list)
        #self.version_list_widget.setFixedSize(100,480)
        #self.version_list_widget.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.version_list_widget.setModel(self.version_list_model)
        self.version_list_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        
        self.version_info=QtGui.QTextBrowser(self)
        self.version_info.setMinimumSize(300,500)
        self.version_info.move(200,20)
        
        
        
        
        
        self.startTimer(1)
        #self.add_to_version_list("Kawser 2")
        #self.add_to_version_list("Kawser 1")
        
        
        #self.menu_bar=
        self.file_menu=self.menuBar().addMenu("&File")
        update_from_file = QtGui.QAction(QtGui.QIcon(os.path.join(getAppPath(),"data/updater/update.png")),"Update From File",self)
        update_from_file.triggered.connect(self.update_from_file)
        self.file_menu.addAction(update_from_file)
        
        
        
        #Signals
        self.CorruptSignal.signal.connect(self.corrupted_signal)
        self.SuccessSignal.signal.connect(self.success_signal)
        self.refresh_vlist()
        
    def refresh_vlist(self):
        QtGui.QApplication.processEvents()
        dirs=os.listdir(self.DIR)
        self.version_list=[]
        for i in dirs:
            if i.endswith(".idat"):
                self.add_to_version_list(i.replace(".idat",""))
#######################################################################

    def success_signal(self):
        QtGui.QMessageBox.information(self,
                                      "Success","Successfully Updated",
                                      QtGui.QMessageBox.Close,
                                      QtGui.QMessageBox.Close)
        
    def corrupted_signal(self):
        QtGui.QMessageBox.information(self,
                                      "corrupted file","The file you have selected is corrupted",
                                      QtGui.QMessageBox.Close,
                                      QtGui.QMessageBox.Close)
    
    
        
    def start_update(self,path):
        """Take care of the update process"""
        #print path
        pid=get_imovman_pid()
        if pid!=False:kill(pid)
        
        fh = open(path, 'rb')
        z = zipfile.ZipFile(fh)
        namelist=z.namelist()
        is_valid=False
        for name in namelist:
            #print name
            if name.find("build-prop.idat")!=-1:
                is_valid=True
                break
        
        
        
        k=ProgressBar()
        def extract_me():
            #global k
            if is_valid:
                ProgressBar.ProgressStarted.signal.emit(len(namelist))
                counter=0
                for name in namelist:
                    #print name
                    counter=counter+1
                    z.extract(name, ".")
                    if name.find("build-prop.idat")!=-1:
                        #z.extract(name,"data/updatelog/kawser.dat")
                        data=form_dict(name)
                        if data.has_key("buildnumber"):
                            fname=data["buildnumber"]+" "+data["buildname"]+" "+data["buildstring"].replace(":","-")
                            shutil.copy(name,"data/updatelog/%s.idat"%fname)
                    ProgressBar.ProgressMessage.signal.emit(str(counter)+" Files Updated")
                    ProgressBar.ProgressReport.signal.emit(counter)
                ProgressBar.ProgressFinished.signal.emit(True)
                self.SuccessSignal.signal.emit()
                self.refresh_vlist()
            else:
                self.CorruptSignal.signal.emit()
    
        thr=threading.Thread(target=extract_me,args=())
        thr.setDaemon(True)
        k.start_progress(thr)
        k.exec_()
        #k.close()
        fh.close()
        
        
        
    def update_from_file(self):
        #print "Updatig From File"

        
        cfile,_ = QtGui.QFileDialog.getOpenFileName(self,self.tr("Select iMovMan Update File"),QtCore.QDir.currentPath(),self.tr("iMovMan Update File(*.ciuf)"))
        if len(cfile)!=0:
            if cfile.endswith("ciuf"):self.start_update(cfile)
            else:QtGui.QMessageBox.information(self,
                                              "Unknown File","The File you have selected \nis not an update file",
                                              QtGui.QMessageBox.Close,
                                              QtGui.QMessageBox.Close)
        else:QtGui.QMessageBox.information(self,
                                          "No Update File Selected","You Have not selected any update file",
                                          QtGui.QMessageBox.Close,
                                          QtGui.QMessageBox.Close)
    def timerEvent(self,event):
        QtGui.QApplication.processEvents()
        #print event
        #print dir(event)
        
        if len(self.version_list_widget.selectedIndexes())!=0:
            if self.selected_item!=self.version_list_widget.selectedIndexes()[0]:
                self.selected_item=self.version_list_widget.selectedIndexes()[0]
                self.version_info.setHtml( self.get_version_string(self.text_from_index(self.selected_item)) )
        #self.killTimer(1)
    
    def text_from_index(self,index):return self.version_list[index.row()]
    
    
    
    
    def get_version_string(self,version):
        path=os.path.join(self.DIR,version+".idat")
        log=open(path,"r")
        clog=""
        for i in read_in_chunks(log):
            clog=clog+i
        clog=clog.replace("\n","<br/>")
        log.close()
        return clog
    
    
    
    def add_to_version_list(self,version):
        QtGui.QApplication.processEvents()
        self.version_list.append(version)
        self.version_list_model.setStringList(self.version_list)
        self.version_list_widget.update()
        
        
    def closeEvent(self,event):
        self.close()
        kill()




























def kill(pid=None):
    """This method is used to kill the app"""
    if pid==None:pid=os.getpid()
    if isWindows():
        try:
            exec("import ctypes")
            exec("PROCESS_TERMINATE = 1")
            exec("handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)")
            exec("ctypes.windll.kernel32.TerminateProcess(handle, -1)")
            exec("ctypes.windll.kernel32.CloseHandle(handle)")
        except:pass
    elif isLinux() or isMac():
        try:
            exec("import signal")
            exec("os.kill(pid, signal.SIGALRM)")
        except:pass

if __name__=="__main__":
    qapp=QtGui.QApplication(sys.argv)
    uw=UpdaterWindow()
    uw.show()
    sys.exit( qapp.exec_() )
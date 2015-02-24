'''
Created on Aug 4, 2013

@author: KaWsEr
'''
from modules.nimovman.core.config import appicon
from modules.nimovman.core import util
from PySide import QtGui,QtCore
from modules.nimovman.core.dbmodel import Trash
from modules.nimovman.core import standardsignal
#import threading
import time

class TrashModel(QtCore.QAbstractTableModel):
    numberPopulated = QtCore.Signal(int)
    def __init__(self,parent=None,*kwards):
        super(TrashModel,self).__init__(parent,*kwards)
        self.__header=["File Name","Path"]
        self.__path_count=0
        self.__path=[]
        self.__download=100
    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.__path_count
        #return self.__path_count
    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self.__header)

    def canFetchMore(self, index):
        return self.__path_count < len(self.__path)
    
    def fetchMore(self, index):
        remainder = len(self.__path) - self.__path_count
        itemsToFetch = min(self.__download, remainder)
        self.beginInsertRows(QtCore.QModelIndex(), self.__path_count,self.__path_count + itemsToFetch)
        self.__path_count += itemsToFetch
        self.endInsertRows()
        self.numberPopulated.emit(itemsToFetch)
        
    def headerData(self, col, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.__header[col]
        return None
    
    def removeRow(self,row,parent=QtCore.QModelIndex()):
        if row<0 or row>self.__path_count:
            return False
        try:
            trash=Trash()
            trash.delete(self.__path[row])
            del self.__path[row]
            self.__path_count-=1
            return True
        except Exception,e:
            print e
            return False
        
    """    
    def removeRows(self, row, count, parent = QtCore.QModelIndex() ):
        # make sure the index is valid, to avoid IndexErrors ;)
        if row < 0 or row > len(self.__path):return False
        self.beginRemoveRows(parent, row, row + count)
        while count != 0:
            try:
                trash=Trash()
                trash.delete(self.__path[row])
                del self.__path[row]
                self.__path_count-=1
                return True
                #print row
            except Exception,e:
                print e
                return False
            count -= 1
        self.endRemoveRows()
        return True
    """
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():return None
        if index.row() >= len(self.__path) or index.row() < 0:return None
        if role == QtCore.Qt.DisplayRole:
            if index.column()==1:return self.__path[index.row()]
            else: return util.get_filename_from_path(self.__path[index.row()])
        if role == QtCore.Qt.BackgroundRole:
            batch = index.row()%2 
            if batch == 0:
                return QtGui.qApp.palette().base()
            return QtGui.qApp.palette().alternateBase()
        return None
    
    def sort(self, Ncol, order):
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        #self.__path = sorted(self.__path, key=operator.itemgetter(Ncol))
        self.__path.sort()
        if order == QtCore.Qt.DescendingOrder:
            self.__path.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))
    
    def set_trash_data(self):
        dtrash=Trash()
        trash=dtrash.get(i=1)
        self.__path=[]
        for item in trash:self.__path.append(item.path)
        #self.__path=["F:\\Kawser.txt"]*10000
        self.__path_count=0
        self.reset()
         
    
class TrashProgress(QtGui.QDialog):
    def __init__(self,parent):
        super(TrashProgress,self).__init__(None)
        self.setWindowIcon(parent.icon)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint|QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)
        TrashWindow.TotalTrashItems.signal.connect(self.total_trash_items)
        TrashWindow.TotalTrashed.signal.connect(self.trashed)
        TrashWindow.TrashingFinished.signal.connect(self.finished)
        self.progress_bar=QtGui.QProgressBar(self)
        self.progress_bar.setFixedWidth(400)
        self.setFixedWidth(400)
        self.setModal(True)
        #self.max=0
        #self.show()

    def total_trash_items(self,number):
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(number)
    def trashed(self,number):
        self.progress_bar.setValue(number)
        if number==1:
            msg="%s Movie Removed From Trash" %number
        elif number>1:
            msg="%s Movies Removed From Trash" %number
        self.setWindowTitle(msg)
        
    def finished(self,b):
        if b:
            time.sleep(0.5)
            self.close()


class TrashWindow(QtGui.QDialog):
    TrashDataReset=standardsignal.SignalInt()
    RemoveRows=QtCore.Signal()
    TotalTrashItems=standardsignal.SignalInt()
    TotalTrashed=standardsignal.SignalInt()
    TrashingFinished=standardsignal.SignalBool()
    def __init__(self,parent=None):
        super(TrashWindow,self).__init__(None)
        self.setWindowTitle("Trash Manager")
        self.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.WindowStaysOnTopHint)
        self.__parent=parent
        self.hide()
        self.setModal(True)
        self.icon=QtGui.QIcon(appicon("iMovMan"))
        self.setWindowIcon(self.icon)
        self.setMinimumHeight(self.height()-self.height()*0.3)
        self.setMinimumWidth(self.width()-self.width()*0.2)
        
        
        self.main_layout=QtGui.QGridLayout()
        self.setLayout(self.main_layout)
        
        self.trash_model=TrashModel(self)
        self.trash_model.set_trash_data()
        self.trash_model.numberPopulated.connect(self.numberPopulated)
        self.trash_table=QtGui.QTableView(self)
        self.main_layout.addWidget(self.trash_table)##Added To Layout
        self.trash_table.setModel(self.trash_model)
        self.trash_table.resizeColumnsToContents()
        #self.trash_table.resizeRowsToContents()
        self.trash_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.trash_table.setShowGrid(False)
        self.trash_table.setSortingEnabled(True)
        
        self.trash_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.trash_table.customContextMenuRequested.connect(self.contextMenuEvent)
                
        hh = self.trash_table.horizontalHeader()#H header
        hh.setStretchLastSection(True)
        vh = self.trash_table.verticalHeader()#V Header
        vh.setVisible(False)
        
        
        ##Signals
        self.TrashDataReset.signal.connect(self.reset_model)
        
        self.logViewer = QtGui.QTextBrowser()
        self.logViewer.setMaximumHeight(100)
        #self.logViewer.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred))
        self.main_layout.addWidget(self.logViewer)
        self.RemoveRows.connect(self.remove_rows)
        
    def contextMenuEvent(self, event):
        #print self.mlist.selectedItems()
        menu = QtGui.QMenu()
        indexlist=self.trash_table.selectedIndexes()
        if len(indexlist)>0:
            untrash=QtGui.QAction(QtGui.QIcon(appicon("default")),"Remove From Trash",self )
            untrash.triggered.connect(self.action_handle)
            menu.addAction(untrash)
        refresh=QtGui.QAction(QtGui.QIcon(appicon("refresh")),"Refresh",self)
        refresh.triggered.connect(self.action_handle)
        menu.addAction(refresh)
        clog=QtGui.QAction(QtGui.QIcon(appicon("act_log")),"Clear Log",self)
        clog.triggered.connect(self.action_handle)
        menu.addAction(clog)
        menu.exec_(QtGui.QCursor.pos())
        
    def action_handle(self):
        act=self.sender().text().lower()
        if act=="refresh":
            self.reset_model(0)
            self.add_msg("Refresh Done.")
        elif act=="clear log":
            self.logViewer.clear()
            
        elif act=="Remove From Trash".lower():

            self.add_msg("Removing From Trash")

            reply = QtGui.QMessageBox.question(self,
                                                   "Remove From Trash?",
                                                   "Do You Really Want it to remove from Trash?",
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            #reply=0
            if reply==QtGui.QMessageBox.Yes:
                k=TrashProgress(self)
                k.show()
                #k.exec_()
                QtGui.QApplication.processEvents()
                self.remove_rows()
                QtGui.QApplication.processEvents()
                #self.RemoveRows.emit()
                """
                try:
                    if not self.rthr.is_alive():
                        self.rthr=threading.Thread(target=self.remove_rows,args=())
                        self.rthr.setDaemon(True)
                        self.rthr.start()
                    else:
                        self.add_msg("Remove From Database is already running. please make the next call after this process")
                except:
                    self.rthr=threading.Thread(target=self.remove_rows,args=())
                    self.rthr.setDaemon(True)
                    self.rthr.start()
                """
                    
            else:
                self.add_msg("Trashing Cancelled...")
                
            
    def numberPopulated(self,number):
        self.add_msg("%s items added"%number)
        
    def remove_rows(self):
        indexlist=self.trash_table.selectedIndexes()
        rows=[]
        #path=[]
        for index in indexlist:
            if index.row() not in rows:
                rows.append(index.row())
                self.add_msg("Removing : %s " %self.trash_table.model().data(index) )
        rows.sort()
        rows.reverse()#Delete From Bottom#
        
        total_trash_items=len(rows)
        self.TotalTrashItems.signal.emit(total_trash_items)
        count=1
        for row in rows:
            self.trash_table.model().removeRow(row)
            self.TotalTrashed.signal.emit(count)
            count=count+1
        self.add_msg("Removing Done..")
        self.TrashingFinished.signal.emit(True)
            
    def add_msg(self,msg):
        self.logViewer.append(msg)
        vs=self.logViewer.verticalScrollBar()
        vs.setValue(vs.maximum())
        #self.logViewer.scroll(100,100)
        
    def reset_model(self,number):
        self.trash_model.set_trash_data()
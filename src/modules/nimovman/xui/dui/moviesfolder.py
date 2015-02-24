'''
Created on Aug 4, 2013

@author: KaWsEr
'''

import os
from PySide import QtGui,QtCore
#from modules.nimovman.core import config
import pickle
from modules.nimovman.core.config import appicon
from modules.nimovman.core.dbmodel import Option
qg=QtGui
qc=QtCore




class MoviesFolder(QtGui.QDialog):
    def __init__(self):
        super(MoviesFolder,self).__init__()
        self.hide()
        self.setWindowTitle("Movie's Folder")
        self.icon=appicon("imovman")
        self.setWindowIcon(qg.QIcon(appicon("imovman")))
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.movie_paths=[]
        self.dirs=[]
        try:
            self.option=Option()
            if self.option.has_option("movie_paths"):
                self.movie_paths=self.option.get_option("movie_paths")
        except Exception,e:
            print e
            self.option=None
        
        if type(self.movie_paths)==list:
            for i in self.movie_paths:
                self.dirs.append((os.path.basename(i),i))
        self.old=self.dirs
        
        layout = qg.QGridLayout() 
        self.setModal(True)
        
        #self.led = QLineEdit("Sample")
        
        self.table = qg.QTableWidget()
        
        self.addButton = qg.QPushButton("Add")
        self.addButton.clicked.connect(self.add_button_method)
        #self.addButton.show()
        
        self.deleteButton = qg.QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete_button_method)
        #self.deleteButton.show()

        self.saveButton = qg.QPushButton("Save")
        self.saveButton.clicked.connect(self.save_button_method)
        self.saveButton.setEnabled(False)
        #self.saveButton.show()
        
        self.reloadButton = qg.QPushButton("Reload")
        self.reloadButton.clicked.connect(self.reload_button_method)
        #self.reloadButton.show()         
        
        button_layout = qg.QGridLayout()
         
        #layout.addWidget(self.led, 0, 0)
        layout.addWidget(self.table, 1, 0)
        button_layout.addWidget(self.addButton,1,0)
        button_layout.addWidget(self.deleteButton,1,1)
        button_layout.addWidget(self.saveButton,1,2)
        button_layout.addWidget(self.reloadButton,1,3)
        
        layout.addLayout(button_layout,2,0)
        
        
        
        self.table.setColumnCount(2)
        
        # Optional, set the labels that show on top
        self.table.setHorizontalHeaderLabels(("Name", "Path"))

        self.update_row()

        #self.table.removeRow(1)
        # Also optional. Will fit the cells to its contents.
        
        #self.table.setColumnWidth(80,20)

        #self.table.setItem(1, 0, QTableWidgetItem(self.led.text()))
        self.setLayout(layout)
        self.setWindowFlags(qc.Qt.CustomizeWindowHint | qc.Qt.WindowTitleHint | qc.Qt.WindowCloseButtonHint)
        
    def update_row(self):
        self.table.setRowCount(len(self.dirs))
        for row, cols in enumerate(self.dirs):
            for col, text in enumerate(cols):
                table_item = qg.QTableWidgetItem(text)
                table_item.setFlags(qc.Qt.ItemIsSelectable|qc.Qt.ItemIsEnabled)
                # Optional, but very useful.
                #table_item.setData(Qt.UserRole+1, user)
                self.table.setItem(row, col, table_item)
        self.table.resizeColumnsToContents()
            
    def add_button_method(self):
        #print "Add Button Clicked"
        #self.movie_paths.append(("n","s"))
        old_size=len(self.old)
        """
        dialog = qg.QFileDialog()
        dialog.setWindowTitle("Select Folder")
        dialog.setWindowIcon(qg.QIcon(self.icon))
        dialog.setFileMode(qg.QFileDialog.Directory)
        dialog.setOption(qg.QFileDialog.ShowDirsOnly)
        #dialog.setOption(QFileDialog.DontUseNativeDialog,True)
        #dialog.
        dialog.exec_()
        
        #print dialog.selectedFiles()
        for i in dialog.selectedFiles():
            p=(os.path.basename(i),os.path.realpath(i))
            if p not in self.dirs:
                self.dirs.append(p)
        """
        #qg.QFileDialog.get
        ##print qc.QDir.
        try:
            path=pickle.load(open("applog/moviesfoldercp.path","rb"))
            path=os.path.dirname(path)
        except:path=qc.QDir.rootPath()#.currentPath()
        #print path

        directory = qg.QFileDialog.getExistingDirectory(self, "Select Folder",path )
        #print directory
        #for i in directory:
        #    print i
        if directory:
            try:
                path=directory
                pickle.dump(path,open("applog/moviesfoldercp.path","wb"))
            except:pass
            p=(os.path.basename(directory),os.path.realpath(directory))
            if p not in self.dirs:
                self.dirs.append(p) 

        
        #print len(self.old),len(self.movie_paths)
        if old_size!=len(self.dirs):
            self.saveButton.setEnabled(True)
        self.update_row()
        self.old=self.dirs
        
    def reload_button_method(self):
        
        self.dirs=[]
        try:self.movie_paths=self.option.get_option("movie_paths")
        except:self.movie_paths=[]
        print self.movie_paths
        if type(self.movie_paths)==list:
            for i in self.movie_paths:
                self.dirs.append((os.path.basename(i),i))
        self.update_row()
        self.old=self.dirs
        
        
    def delete_button_method(self):
        #print "Delete Button Clicked"
        #print self.table.selectedItems()
        #print self.table.selectedIndexes()
        
        #for i in self.table.selectedIndexes():
        #    print i
        #"""
        old_size=len(self.old)
        for i in self.table.selectedItems():
            try:
                row=self.table.row(i)
                self.table.removeRow(row)
                del self.dirs[row]
            except:pass
        print self.dirs
        
        if old_size!=len(self.dirs):
            self.saveButton.setEnabled(True)
        self.old=self.dirs
        #"""
    
    def save_button_method(self):
        #print "Save Button Method"
        movie_list=[]
        for i in self.dirs:
            movie_list.append(i[1])
        try:
            self.option.replace("movie_paths", movie_list)
            self.saveButton.setEnabled(False)
            self.old=self.dirs
        except Exception,e:
            print e
            
    def closeEvent(self,evnt):
        self.hide()
        #if not self.main_window.file_crawler.isRunning():
        #    self.main_window.status.setText("Scan initializing...")
        #    thr = threading.Thread(target=self.main_window.file_crawler.run)
        #    thr.daemon = True
        #    thr.start()
        #evnt.ignore()
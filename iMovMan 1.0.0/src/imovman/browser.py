'''
Created on May 24, 2013

@author: KaWsEr
'''

import os
import ast
import sys
import idb
import crawler
#import time
#import threading
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *




import config
from config import appicon,appanim


import utility
import threading
import webbrowser


import urllib2

import json
import socket

#default_timeout = 4

#socket.setdefaulttimeout(default_timeout)


qApp=None



class SignalObject(QObject):
    sig = Signal(bool)





def has_update():
    data={}
    try:
        u = urllib2.urlopen(config.APP_UPDATE_CHECK)
        data=json.load(u)
        u.close()
    except Exception,e:
        print e
        data={}
    if data.has_key("v"):
        #print data["v"]
        if data["v"]==config.APP_VERSION:return (False,data["v"])
        else:return (True,data["v"])
    else:return (False,config.APP_VERSION)




class BrowserWindow(QWebView):
    def __init__(self,url,mainwindow,parent=None):
        super(BrowserWindow, self).__init__(parent)
        self.url=url
        self.mainwindow=mainwindow
        self.setZoomFactor(0.9)
        
        
        self.loadStarted.connect(self.load_started)
        self.setUrl(self.url)
        #self.load(QUrl(self.url))
        #self.loadFinished.
        #mainwindow.spinner.stop()
        #mainwindow.add_msg("WHat")

        self.loadProgress.connect(self.load_pg)
        self.loadFinished.connect(self.load_finished)
    
    def load_started(self):
        print "Started"
        self.mainwindow.spin_start()
    def load_finished(self):
        print "Load Finished...."
        self.mainwindow.spin_stop()

    def load_pg(self,progress):
        #print progress
        if progress!=100:
            self.mainwindow.spin_start()
        if progress==100:
            self.mainwindow.spin_stop()
        
        
###################################
class MovieFormat(QDialog):
    def __init__(self,icon, parent=None):
        super(MovieFormat, self).__init__(parent)
        self.icon=icon
        self.setWindowTitle("Movie Format")
        self.setWindowIcon(QIcon(icon))
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        
        self.movie_format=[]
        self.cdb=idb.CDb()
        if self.cdb.has_key("movie_format"):
            self.movie_format=ast.literal_eval(self.cdb.get("movie_format").value)
        else:
            self.movie_format=[]
        #print self.movie_list
        
        self.old=self.movie_format
        #self.movie_paths=[("F:/","Movies World"),("G","What")]
        
        layout = QGridLayout() 
        
        
        #self.led = QLineEdit("Sample")
        
        self.table = QTableWidget()
        
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.add_button_method)
        #self.addButton.show()
        
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete_button_method)
        #self.deleteButton.show()

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save_button_method)
        self.saveButton.setEnabled(False)
        #self.saveButton.show()
        
        self.reloadButton = QPushButton("Reload")
        self.reloadButton.clicked.connect(self.reload_button_method)
        #self.reloadButton.show()         
        
        button_layout = QGridLayout()
         
        #layout.addWidget(self.led, 0, 0)
        layout.addWidget(self.table, 1, 0)
        button_layout.addWidget(self.addButton,1,0)
        button_layout.addWidget(self.deleteButton,1,1)
        button_layout.addWidget(self.saveButton,1,2)
        button_layout.addWidget(self.reloadButton,1,3)
        
        layout.addLayout(button_layout,2,0)
        
        
        
        self.table.setColumnCount(1)
        
        # Optional, set the labels that show on top
        self.table.setHorizontalHeaderLabels(("Format",))

        self.update_row()

        #self.table.removeRow(1)
        # Also optional. Will fit the cells to its contents.
        
        #self.table.setColumnWidth(80,20)

        #self.table.setItem(1, 0, QTableWidgetItem(self.led.text()))
        self.setLayout(layout)
        
    def update_row(self):
        self.table.setRowCount(len(self.movie_format))
        for row,text in enumerate(self.movie_format):
            table_item = QTableWidgetItem(text)
            table_item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            # Optional, but very useful.
            #table_item.setData(Qt.UserRole+1, user)
            self.table.setItem(row,0, table_item)
        self.table.resizeColumnsToContents()
        print self.movie_format
            
    def add_button_method(self):
        print "Add Button Clicked"
        #self.movie_paths.append(("n","s"))
        old_size=len(self.old)
        
        text, result = QInputDialog.getText(self, "Movie File Format Input Box","Enter The extension of movie file format:")
        if result:
            if text!=None or text!=" ":
                text=text.replace(" ","")
                if text!=u"":
                    if text.lower() not in self.movie_format:
                        self.movie_format.append(text.lower())
            
        self.update_row()
        
        if old_size!=len(self.movie_format):
            self.saveButton.setEnabled(True)
        self.old=self.movie_format
        
    def reload_button_method(self):
        
        self.movie_format=[]
        if self.cdb.has_key("movie_format"):
            self.movie_format=ast.literal_eval(self.cdb.get("movie_format").value)
        else:
            self.movie_format=[]
        self.update_row()
        self.old=self.movie_format
        
        
    def delete_button_method(self):
        print "Delete Button Clicked"
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
                del self.movie_format[row]
            except:pass
        print self.movie_format
        
        if old_size!=len(self.movie_format):
            self.saveButton.setEnabled(True)
        self.old=self.movie_format
        #"""
    
    def save_button_method(self):
        print "Save Button Method"
        self.cdb.add("movie_format",self.movie_format)
        self.saveButton.setEnabled(False)
        self.old=self.movie_format
            
            
    # Greets the user
    def greetings(self):
        print ("Hello %s" % self.edit.text())

########################################
class ThemeChooser(QDialog):
    def __init__(self,parent=None):
        super(ThemeChooser, self).__init__(parent)
        self.setWindowTitle("Theme Chooser")
        self.setWindowIcon(QIcon(appicon("imovman-32x32")))
        
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
    


######################################
class MoviesFolder(QDialog):
    def __init__(self,icon, parent=None):
        super(MoviesFolder, self).__init__(parent)
        self.icon=icon
        self.setWindowTitle("Movies Folder")
        self.setWindowIcon(QIcon(icon))
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.movie_paths=[]
        self.cdb=idb.CDb()
        if self.cdb.has_key("movie_path"):
            self.movie_list=ast.literal_eval(self.cdb.get("movie_path").value)
        else:
            self.movie_list=[]
        #print self.movie_list
        
        
        if type(self.movie_list)==list:
            for i in self.movie_list:
                self.movie_paths.append((os.path.basename(i),i))
        self.old=self.movie_paths
        #self.movie_paths=[("F:/","Movies World"),("G","What")]
        
        layout = QGridLayout() 
        
        
        #self.led = QLineEdit("Sample")
        
        self.table = QTableWidget()
        
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.add_button_method)
        #self.addButton.show()
        
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete_button_method)
        #self.deleteButton.show()

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save_button_method)
        self.saveButton.setEnabled(False)
        #self.saveButton.show()
        
        self.reloadButton = QPushButton("Reload")
        self.reloadButton.clicked.connect(self.reload_button_method)
        #self.reloadButton.show()         
        
        button_layout = QGridLayout()
         
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
        
    def update_row(self):
        self.table.setRowCount(len(self.movie_paths))
        for row, cols in enumerate(self.movie_paths):
            for col, text in enumerate(cols):
                table_item = QTableWidgetItem(text)
                table_item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                # Optional, but very useful.
                #table_item.setData(Qt.UserRole+1, user)
                self.table.setItem(row, col, table_item)
        self.table.resizeColumnsToContents()
            
    def add_button_method(self):
        print "Add Button Clicked"
        #self.movie_paths.append(("n","s"))
        old_size=len(self.old)
        dialog = QFileDialog()
        dialog.setWindowTitle("Select Folder")
        dialog.setWindowIcon(QIcon(self.icon))
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        #dialog.setOption(QFileDialog.DontUseNativeDialog,True)
        #dialog.
        dialog.exec_()
        
        #print dialog.selectedFiles()
        for i in dialog.selectedFiles():
            p=(os.path.basename(i),os.path.realpath(i))
            if p not in self.movie_paths:
                self.movie_paths.append(p)
            

        
        #print len(self.old),len(self.movie_paths)
        if old_size!=len(self.movie_paths):
            self.saveButton.setEnabled(True)
        self.update_row()
        self.old=self.movie_paths
        
    def reload_button_method(self):
        
        self.movie_paths=[]
        if self.cdb.has_key("movie_path"):
            self.movie_list=ast.literal_eval(self.cdb.get("movie_path").value)
        else:
            self.movie_list=[]
        if type(self.movie_list)==list:
            for i in self.movie_list:
                self.movie_paths.append((os.path.basename(i),i))
        self.update_row()
        self.old=self.movie_paths
        
        
    def delete_button_method(self):
        print "Delete Button Clicked"
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
                del self.movie_paths[row]
            except:pass
        print self.movie_paths
        
        if old_size!=len(self.movie_paths):
            self.saveButton.setEnabled(True)
        self.old=self.movie_paths
        #"""
    
    def save_button_method(self):
        print "Save Button Method"
        movie_list=[]
        for i in self.movie_paths:
            movie_list.append(i[1])
        self.cdb.add("movie_path",movie_list)
        self.saveButton.setEnabled(False)
        self.old=self.movie_paths
            
            
    # Greets the user
    def greetings(self):
        print ("Hello %s" % self.edit.text())



### About Dialog ###
class AboutDialog(QMessageBox):
    def __init__(self):
        super(AboutDialog,self).__init__()
        self.setWindowTitle("About "+config.APP_NAME)
        self.setWindowIcon(QIcon(config.appicon("imovman-32x32")))
        #self.baseSize()
        #self.setFixedHeight(500)
        #self.setFixedWidth(500)
        #"""
        self.setFixedSize(QSize(500,500))
        rect=self.geometry()
        rect.moveCenter(qApp.desktop().availableGeometry().center())
        self.setGeometry(rect)
        #self.setFixedSize(self.size())
        
        #print "On About Dialog"
        about_text="""
        
        <b>%s %s</b><br/>
        <b>CodeName : %s</b><br/>
        <b>Developer : %s</b><br/>
        
        <br/><br/><br/>%s<br/><br/>
        
        For More Information and Help Visit Our HomePage<br/>
        <div><center><a href="%s">%s</a></center>
        <br/>
        %s
        </div>
        """%(config.APP_NAME,
             config.APP_VERSION,
             config.APP_CODENAME,
             config.APP_DEVELOPER,
             config.APP_DESCRIPTION,
             config.APP_WEB,
             config.APP_WEB_LABEL,
             config.APP_COPYRIGHT)
        #print about_text     
        self.setText(about_text)
        #self.setDetailedText("asjiaso sd")
        #rect.moveCenter(qApp.desktop().availableGeometry().center())
        #self.setGeometry(rect)
        #self.setFixedSize(self.size())
        
        self.setStyleSheet("QDialog {background: 'white';}")
        self.show()
        #print "On About Dialog End"
###############################

"""The MainWindow Handler"""
class MainWindow(QMainWindow):
    def __init__(self,qapp,url):
        super(MainWindow, self).__init__()
        
        #self.idb=idb.IDb()#Information Database Handler#
        #self.cdb=idb.CDb()#Configuration Database Handler#
        load_signal=SignalObject()
        load_signal.sig.connect(self.mainwindow_loaded)
        
        self.qapp=qapp
        self.url=url
        self.icon=config.appicon("imovman-32x32")

        
        
        
        #print self.has_update,self.version
        ##Window Settings
        self.setWindowTitle('iMovMan')
        self.setWindowIcon(QIcon(self.icon))
        #self.showMaximized()
        
        #self.setFixedSize(self.size())
        #print self.width()
        self.desktop=self.qapp.desktop()
        self.screenWidth=self.desktop.width()
        self.screenHeight=self.desktop.height()
        
        
        
        #self.mnmsize=QSize(self.width()-self.width()*0.01,self.height()-self.height()*0.20)
        #self.setMinimumSize(self.mnmsize)
        self.sysTray()
        self.WindowMenuBar()
        
        ###### Widget Collection#########
        self.main_widget=QWidget(self)
        
        self.spinner = QMovie(appanim("anim"), QByteArray(), self)
        self.spinner.setCacheMode(QMovie.CacheAll)
        self.spinner.setSpeed(100)
        
        self.stbar = QStatusBar(self)#StatusBar
        
        self.scanner = QLabel("")
        self.scanner.setMaximumWidth(200)
        
        self.spinner_screen = QLabel()
        self.spinner_screen.hide()
        #self.movie.setSpeed(100)
        self.spinner_screen.setMinimumWidth(20)
        self.spinner_screen.setMaximumWidth(20)
        self.spinner_screen.setMovie(self.spinner)
        
        self.statusbar_widget=QWidget(self)#add this to main layout
        self.statusbar_widget.setMaximumHeight(20)
        #self.statusbar_widget.height(20)
        
        self.main_layout = QVBoxLayout()#this contains all widget
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        
        
        

        
        
        
        
        
        

        
        
        
        self.main_widget.setLayout(self.main_layout)
        
        

        #self.web.show()
        #self.main_layout.
        
        #self.setLayout(self.main_layout)
        
        #self.web.show()
        #self.web.reload()
        

        
        
        self.statusbar_layout = QHBoxLayout()#contains all statusbar widget
        self.statusbar_layout.setSpacing(0)
        self.statusbar_layout.setContentsMargins(0, 0, 0, 0)
        #self.statusbar_layout.
        self.statusbar_widget.setLayout(self.statusbar_layout)
        
        
        
        self.statusbar_layout.addWidget(self.stbar)
        
        self.statusbar_layout.setSpacing(5)
        
        

        self.statusbar_layout.addWidget(self.scanner)
        #self.scanner.setText("kaw")
        

        
        
        #self.spinner_screen.show()
        
        
        self.statusbar_layout.addWidget(self.spinner_screen)
        #self.statusbar_layout.addWidget(QLabel("What"))
        #self.statusbar_layout.addWidget(QLabel("What"))
        #self.statusbar_layout.addWidget(QLabel("What"))
        #self.stbar.setMaximumHeight(10)
        
        
        #self.main_widget = self.web
        #self.main_layout = QVBoxLayout(self.main_widget)
        #self.main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        #self.main_layout.addWidget(self.main_widget) 
        #form_widget has its own main_widget where I put all other widgets onto

        #self.main_widget.setLayout(self.main_layout)
        #self.setCentralWidget(self.main_widget)
        #self.show()
        #self.statusBar().showMessage("Ready")
        
        self.setCentralWidget(self.main_widget)
        self.stbar.showMessage("Ready.")
        
        
        
        
        ######
        self.crawler=crawler.FileCrawler(self)
        #self.crawler.signal.sig.connect(self.spin_stop)
        
        #self.has_update=False
        
        #########################################################
        #if application has update do something here
        
        #load_signal.sig.emit(True)
        #self.spin_start()
        self.web=BrowserWindow(self.url,self)
        self.main_layout.addWidget(self.web)
        self.main_layout.addWidget(self.statusbar_widget)
        
        
        load_signal.sig.emit(True)
    
    
    
    def mainwindow_loaded(self,b):
        if b:
            
            self.spin_start()
            self.has_update,self.version=has_update()
            print "Update Check Started..."
            #self.update_check()

            
    def statusBar(self):
        return self.stbar    
    def add_msg(self,msg):
        self.stbar.showMessage(msg)    
    def resizeEvent(self,resizeEvent):
        pass
        #QMessageBox.information(self,"Information!","Window has been resized...")
        #self.web.reload()
        #self.centerMe()
        
    def centerMe(self):
        windowSize = self.size()#size of our application window
        width = windowSize.width()
        height = windowSize.height()
        x = (self.screenWidth-width)/2
        y = (self.screenHeight-height) / 2
        y -= 50
        self.move(x,y)
        
    def WindowMenuBar(self):
        """Window Menu Bar"""
        self.menubar = self.menuBar()
        
        ##File Menu
        self.fileMenu = self.menubar.addMenu('&File')
        
        
        self.folderScanAction=QAction(QIcon(appicon("folder_scan")),'&Scan', self)
        self.folderScanAction.setShortcut('Ctrl+S')
        self.folderScanAction.triggered.connect(self.folder_scan)
        self.folderScanAction.setStatusTip('Scan Folder for Movies')
        
        self.fileMenu.addAction(self.folderScanAction)
        
        self.openInBrowserAction=QAction(QIcon(appicon("browser")),'&Open in Browser', self)
        self.openInBrowserAction.triggered.connect(self.open_in_browser)
        self.openInBrowserAction.setShortcut('Ctrl+O')
        self.fileMenu.addAction(self.openInBrowserAction)
        
        self.exitAction = QAction(QIcon(appicon("exit")),'&Exit', self)        
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.qapp.quit)
        self.fileMenu.addAction(self.exitAction)
        
        ##Edit Menu
        self.editMenu=self.menubar.addMenu('&Edit')
        
        self.settingsAction=QAction(QIcon(appicon("settings")),'&Settings', self)
        ####self.editMenu.addAction(self.settingsAction)
        

        
        
        
        ###Options
        self.optionsMenu=self.menubar.addMenu('&Options')
        
        self.themeAction=QAction(QIcon(appicon("themes")),'&Themes', self)
        self.themeAction.triggered.connect(self.themes)
        ####self.optionsMenu.addAction(self.themeAction)
        
        self.moviesFolderAction=QAction(QIcon(appicon("movie_folder")),'&Movies Folder', self)
        self.moviesFolderAction.triggered.connect(self.movies_folder)
        self.optionsMenu.addAction(self.moviesFolderAction)
        
        self.movieFormatAction=QAction(QIcon(appicon("file_type")),'&Movie File Format', self)
        self.movieFormatAction.triggered.connect(self.movie_format)
        self.optionsMenu.addAction(self.movieFormatAction)

        
        
        
        
        ##Help Menu
        self.helpMenu=self.menubar.addMenu('&Help')
        
        ##Actions##
        self.aboutAction=QAction(QIcon(appicon("about")),'&About', self)
        self.aboutAction.triggered.connect(self.about_window)
        self.helpMenu.addAction(self.aboutAction)
        
        #################
    def update_check(self):
        if self.has_update:
            reply = QMessageBox.question(self, "New Version Released ","Your Current Version is : "+config.APP_VERSION+"\nNew version Found : "+self.version+"\nDo You Want to update?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            #print reply
            if reply == QMessageBox.Yes:
                webbrowser.open_new(config.APP_WEB)
            else:pass
            #super(MainWindow, self).closeEvent(evnt)
        #elif reply == QMessageBox.No:
        #    evnt.ignore()
        
    def about_window(self):
        eobj=AboutDialog()
        eobj.exec_()
        #eobj.show()
    def open_in_browser(self):
        webbrowser.open_new(self.url)
        
    def folder_scan(self):
        print "Folder Scan Triggered"
        if not self.crawler.isRunning():
            #if not self.crawler._Thread__started:
                #self.crawler._Thread__started=False
            #self.spin_start()
            #self.crawler.start()
            thr = threading.Thread(target=self.crawler.run)
            thr.daemon = True
            thr.start()
            #else
            #self.crawler
        print "Folder Scan Started...."
    def spin_start(self):
        self.spinner_screen.show()
        self.spinner.start()
        
    def spin_stop(self):
        self.spinner.stop()
        self.spinner_screen.hide()    
    def themes(self):
        print "Theme Triggered"
        thmc=ThemeChooser(self)
        thmc.show()
    def movie_format(self):
        mf=MovieFormat(self.icon,self)
        mf.show()
    def movies_folder(self):
        mf=MoviesFolder(self.icon,self)
        mf.show()   
    def sysTray(self):
        ####System Try Settings######
        self.systray=QSystemTrayIcon()
        self.systray.setIcon( QIcon(self.icon) )
        self.systray.show()
        self.systray.activated.connect(self.activate)
        
        self.menu = QMenu()
        self.connect(self.menu.addAction("Open"),SIGNAL('triggered()'),self.mopen)
        self.connect(self.menu.addAction("Exit"),SIGNAL('triggered()'),self.mexit)
        
        self.systray.setContextMenu(self.menu)
        
    def mopen(self):
        self.centerMe()
        self.show()
    def mexit(self):self.qapp.exit()
    
    def activate(self,reason):
        #print reason
        if reason==2:
            self.show()
        elif reason==3:
            self.show()
            
    def __icon_activated(self, reason):
        #print dir(QtGui.SystemTrayIcon)
        if reason == QSystemTrayIcon.DoubleClick:
            self.maximize()
            self.show()
            
            
    def maximize(self):
        #self.windowState()
        #self.centerMe()
        self.windowState(Qt.WindowMaximized)
    
    def minimize(self):
        #self.centerMe()
        self.windowState(Qt.WindowMinimized)
    
    
    def keyPressEvent(self,evnt):
        cz=self.web.zoomFactor()
        if evnt.text().lower()=="z":
            self.web.setZoomFactor(cz+0.1)
            
        if evnt.text().lower()=="x":
            self.web.setZoomFactor(cz-0.1)
            
        if evnt.text().lower()=="c":
            self.web.setZoomFactor(0.9)
                    
    def closeEvent(self, evnt):
        reply = QMessageBox.question(self, 'System Tray',"Jump to system tray?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #print reply
        if reply != QMessageBox.Yes:
            evnt.accept()
            super(MainWindow, self).closeEvent(evnt)
        #elif reply == QMessageBox.No:
        #    evnt.ignore()
        else:
            self.systray.show()
            self.hide()
            evnt.ignore()
        """    
        if self._want_to_close:super(BrowserWindow, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.setWindowState(Qt.WindowMinimized)
            #self.hide()
        """    



########################################################


"""The Application Handler every thing should be here"""
class uWindow(object):
    def __init__(self,url):
        self.qapp = QApplication(sys.argv)
        global qApp
        qApp=self.qapp
        ld=os.path.realpath(os.path.join(utility.get_app_path(),"imageformats/"))
        if os.path.exists(ld):
            self.qapp.addLibraryPath(ld)
        splash=QSplashScreen(QPixmap(config.appsplash("imovman")), Qt.WindowStaysOnTopHint)
        splash.show()
        splash.showMessage("Loading.....",Qt.AlignLeft | Qt.AlignBottom, Qt.red);
        self.qapp.processEvents()
        
        self.url=url
        
        self.sFlag=True
        #splash.showMessage('Loading ...')
        #time.sleep(1)
        #self.my=my()
        #splash.finish(self.my)
        #has_upd,v=has_update()
        self.mainwindow=MainWindow(self.qapp,self.url)
        #self.mainwindow.spinner.start()
        
        
        QThread.sleep(1)
        
        splash.finish(self.mainwindow)
        QThread.sleep(0.5)
        self.mainwindow.showMaximized()
        self.mainwindow.update_check()
        #self.mainwindow.show()
        #self.mainwindow.spinner.stop()
        self.mainwindow.spinner.stop()
        
    
    
    def start(self):
        self.qapp.exec_()
            
    def show(self):
        self.sFlag=True
        self.mainwindow.show()
        #self.mainwindow.web.show()
        #self.web.maximize()
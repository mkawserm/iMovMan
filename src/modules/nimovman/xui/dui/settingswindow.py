'''
Created on Aug 4, 2013

@author: KaWsEr
'''
import os
#import re
from modules.nimovman.core import util
from PySide import QtGui,QtCore



from modules.nimovman.core import config

from modules.nimovman.core.config import appicon
from modules.nimovman.core.dbmodel import Option
qg=QtGui
qc=QtCore
#import time

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def format_string(msg):
    msgl=msg.split(" ")
    
    temp=""
    msgn=""
    for i in msgl:
        temp=temp+i+" "
        if len(temp)>=25:
            msgn=msgn+temp+"\n"
            temp=""
    return msgn+temp

def get_title_hints(tstr):
    #tstr="Smile"
    rlist=[]
    for i in config.ALLOWED_IN_TITLE:
        temp="%"+i+"%"
        if tstr.find(temp)!=-1:
            rlist.append(i)
    return rlist
    
            

tool_tip={}
tool_tip["cover_dir"]="Where do You want to save movie covers?"
tool_tip["data_dir"]="iMovMan saves IMDb information into a text file. Where do you want to save this small text file"
tool_tip["auto_scan"]="""If it is enabled you do not need to manually scan movies. It Will automatically scan and add movies"""
tool_tip["auto_delete"]="""If it is enabled non existing movies will be automatically deleted from the database"""
tool_tip["copy_command"]="If you want to use other copy utility (ex: TeraCopy) set it here properly. For more help press F1"
tool_tip["title_style"]="How the movie title will be shown on main page ex: %title% (%year%). For more Help press F1"
tool_tip["movie_api"]="Movie's Api contain the movie information fetcher logic. Set Your desired movie fetcher logic distributed by cliodin.com"
tool_tip["send_to"]="This settings is applicable for when sending a movie to pen drives or other logical drives and determine how the sending system will be performed"
for key in tool_tip.keys():
    tool_tip[key]=format_string(tool_tip[key])








class SWItem(qg.QWidget):
    def __init__(self,title,options,callback,parent):
        super(SWItem,self).__init__(parent)
        self.setContentsMargins(5,5,5,5)
        self.setStyleSheet("""
        .QWidget{border:5px solid black;
        }
        """)
        self.main_container=qg.QHBoxLayout()
        self.setObjectName("SWItem")
        self.main_container.setContentsMargins(0,0,0,0)

        self.title=qg.QLabel(title,self)
        self.title.setStyleSheet("QLabel{color:white;font:bold 10pt}")

        
        self.options=qg.QComboBox()
        for i in options:
            self.options.addItem(i)
        self.options.activated.connect(callback)
        
        self.main_container.addWidget(self.title)
        self.main_container.addWidget(self.options)
        #self.cover_dir_container.addWidget(self.cover_dir_options) 
        #self.cover_dir_widget.setLayout(self.cover_dir_container)
        self.setLayout(self.main_container)
        
        
    def enterEvent(self,event):
        #print "Entered"
        pass
    def leaveEvent(self,event):pass
        #print "Leave Event"
        #self.setStyleSheet("")
    def paintEvent(self,event):
        #print event
        #print "Paint Event"
        #print dir(event)
        painter=qg.QPainter(self)
        #k=qg.QColor(107, 58, 154)
        k=qg.QColor(58, 170, 255)

        background=qg.QBrush(k)
        painter.setBrush(background)
        painter.setPen  (qc.Qt.SolidLine)
        #painter.drawRoundedRect(0,0,self.width(),self.height(),3,3)
        #painter.drawRect(0, 0, self.width(), self.height())

class SWItemEdit(qg.QWidget):
    def __init__(self,title,callback,parent):
        super(SWItemEdit,self).__init__(parent)
        self.setContentsMargins(5,5,5,5)
        self.main_container=qg.QHBoxLayout()
        self.setObjectName("SWItemEdit")
        self.main_container.setContentsMargins(0,0,0,0)

        self.title=qg.QLabel(title,self)
        self.title.setFixedWidth(150)
        self.title.setStyleSheet("QLabel{color:white;font:bold 10pt}")

        self.edit=qg.QLineEdit(self)
        #self.edit.setFixedWidth(100)
        self.edit.textEdited.connect(self.edited)
        self.edit.textChanged.connect(self.edited)
        #self.edit.editingFinished.connect(callback)
        self.button=qg.QPushButton("Save",self)
        self.button.setEnabled(False)
        self.button.clicked.connect(callback)
        self.main_container.addWidget(self.title)
        self.main_container.addWidget(self.edit)
        self.main_container.addWidget(self.button)
        #self.cover_dir_container.addWidget(self.cover_dir_options) 
        #self.cover_dir_widget.setLayout(self.cover_dir_container)
        self.setLayout(self.main_container)
        
    def edited(self,*kwards,**kwargs):
        self.button.setEnabled(True)

class SettingsWindow(QtGui.QDialog):
    def __init__(self,parent):
        self.__parent=parent
        self.mainwindow=parent
        super(SettingsWindow,self).__init__()
        self.hide()
        #self.Wi
        self.setModal(True)
        self.setObjectName("SettingsWindow")
        #self.setStyleSheet(style)
        #self.setSpacing(0)
        self.setContentsMargins(0,0,0,0)
        ## Non Gui ##
        try:self.option=Option()
        except:self.option=None        
        
        self.setWindowFlags(qc.Qt.WindowTitleHint|qc.Qt.WindowCloseButtonHint)
        self.setWindowTitle(config.APP_NAME+" ::: "+"Settings")
        self.icon=appicon("imovman")
        self.setWindowIcon(qg.QIcon(self.icon))
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setFixedSize(500,500)
        
        self.re_init()


    def keyPressEvent(self,evnt):
        if evnt.key()==qc.Qt.Key_F1:
            try:
                ins=self.__parent
                ins.keyPressEvent(evnt)
            except Exception,e:
                print e
                
    def showEvent(self,event):
        self.center()
        
    def paintEvent(self,event):
        painter=qg.QPainter(self)
        #k=qg.QColor(107, 58, 154)
        k=qg.QColor(58, 170, 255)

        background=qg.QBrush(k)
        painter.setBrush(background)
        painter.setPen  (qc.Qt.NoPen )
        painter.drawRect(0, 0, self.width(), self.height())
      


        
    def re_init(self):
        self.block=qg.QSpacerItem(self.width(),self.height())
        
        self.tab_widget = QtGui.QTabWidget()
        
        self.tab_widget.setStyleSheet("""
        QTabWidget::pane { /* The tab widget frame */
        border-top: 2px solid black;
        background-color: #29615a;
        }
        
        QTabWidget::tab-bar {
        alignment: left;
        background: #3E3E3E;
        }
        
        QTabBar::tab {
        width:250px;
        /*border-right: 1px solid black;*/
        background: #db701a;
        color: #defdf5;
        padding: 10px 0px 10px 0;
        font: 75 10pt "Source Sans Pro";
        }
        
        QTabBar::tab:hover {
        background-color: rgb(85, 170, 255);
        }
        
        QTabBar::tab:selected {
        background: grey;
        color:white;
        }
        
        """)
        
        self.basic_tab = QtGui.QWidget()
        self.basic_tab.setContentsMargins(0,0,0,0)
        self.basic_tab_container = qg.QGridLayout(self.basic_tab)
        #self.basic_tab_container = QtGui.QVBoxLayout(self.basic_tab)
        
        cdir=config.DATA_DIR[0]
        ddir=config.DATA_DIR[0]
        try:
            cdir=self.option.get_option("cover_dir")
            ddir=self.option.get_option("data_dir")
        except:pass
        
        self.cover_dir_options=[]
        self.cover_dir_options.append(cdir)
        
        self.data_dir_options=[]
        self.data_dir_options.append(ddir)
        
        for i in config.DATA_DIR:
            if i!=cdir:
                self.cover_dir_options.append(i)
            if i!=ddir:
                self.data_dir_options.append(i)
    
        self.cover_dir_widget=SWItem("Cover Directory: ",self.cover_dir_options,self.cover_dir_click,self)
        self.cover_dir_widget.setToolTip(tool_tip["cover_dir"])
        self.cover_dir_custom=qg.QLabel("",self)
        self.cover_dir_custom.setStyleSheet("""
        QLabel{
        color:yellow;
        font:bold 10pt;
        border:1px solid black;
        border-radius:5px;}""")
        self.cover_dir_custom.hide()
        try:
            if self.option.has_option("cover_dir_custom"):
                self.cover_dir_custom.setText(self.option.get_option("cover_dir_custom"))
                self.cover_dir_custom.show()
        except:pass
        #self.cover_dir_widget.options.setToolTip(tool_tip["cover_dir"])
        self.basic_tab_container.addWidget(self.cover_dir_widget)
        self.basic_tab_container.addWidget(self.cover_dir_custom)
        
        
        
        self.data_dir_widget=SWItem("Text Data Directory: ",self.data_dir_options,self.data_dir_click,self)
        self.data_dir_widget.setToolTip(tool_tip["data_dir"])
        self.data_dir_custom=qg.QLabel("",self)
        self.data_dir_custom.setStyleSheet("""
        QLabel{
        color:yellow;
        font:bold 10pt;
        border:1px solid black;
        border-radius:5px;}""")
        self.data_dir_custom.hide()
        try:
            if self.option.has_option("data_dir_custom"):
                self.data_dir_custom.setText(self.option.get_option("data_dir_custom"))
                self.data_dir_custom.show()
        except:pass
        #self.data_dir_widget.options.setToolTip(tool_tip["data_dir"])
        
        self.basic_tab_container.addWidget(self.data_dir_widget)
        self.basic_tab_container.addWidget(self.data_dir_custom)
        
        
        cas=config.EN_DIS[1]
        cad=config.EN_DIS[1]
        self.auto_scan_options=[]
        self.auto_delete_options=[]
        try:
            cas=self.option.get_option("auto_scan")
            cad=self.option.get_option("auto_delete")
        except:pass
        self.auto_scan_options.append(cas)
        self.auto_delete_options.append(cad)
        for i in config.EN_DIS:
            if i!=cas:
                self.auto_scan_options.append(i)
            if i!=cad:
                self.auto_delete_options.append(i)
            

        self.auto_scan_widget=SWItem("Auto Add Movies:",self.auto_scan_options,self.auto_scan_click,self)        
        self.auto_scan_widget.setToolTip(tool_tip["auto_scan"])
  
        
        self.basic_tab_container.addWidget(self.auto_scan_widget)
        

        self.auto_delete_widget=SWItem("Auto Delete Movies:",self.auto_delete_options,self.auto_delete_click,self)
        
        self.auto_delete_widget.setToolTip(tool_tip["auto_delete"])
        #self.auto_delete_widget.options.setToolTip(tool_tip["auto_delete"])
        self.basic_tab_container.addWidget(self.auto_delete_widget)
        
        
        
        
        self.send_to_options=[]
        try:sto=self.option.get_option("send_to")
        except:sto=None
        if sto!=None:self.send_to_options.append(sto)
        for i in config.SEND_TO:
            if i!=sto:self.send_to_options.append(i)
        
        self.send_to=SWItem("Send To Type: ",self.send_to_options,self.send_to_callback,self)
        self.send_to.setToolTip(tool_tip["send_to"])
        self.basic_tab_container.addWidget(self.send_to)
        
        
        
        ### Advanced Tab Container
        self.advanced_tab = QtGui.QWidget()
        self.advanced_tab_container = QtGui.QVBoxLayout(self.advanced_tab)
        
        self.copy_command=SWItemEdit("Copy Command: ",self.copy_command_callback,self)
        self.copy_command.setToolTip(tool_tip["copy_command"])
        try:cc=self.option.get_option("copy_command")
        except:cc=None
        if cc!=None:self.copy_command.edit.setText(cc)
        self.copy_command.button.setEnabled(False)


        self.advanced_tab_container.addWidget(self.copy_command)
        
        self.title_style=SWItemEdit("Title Style: ",self.title_style_callback,self)
        self.title_style.setToolTip(tool_tip["title_style"])
        try:ts=self.option.get_option("title_style")
        except:ts=None
        if ts!=None:self.title_style.edit.setText(ts)
        self.title_style.button.setEnabled(False)
        #self.advanced_tab_container.addWidget(self.title_style)
        
        self.movie_fetcher_apis_options=[]
        try:mfa=self.option.get_option("movie_api")
        except:mfa=None
        if mfa!=None:self.movie_fetcher_apis_options.append(mfa)
        for i in util.get_movie_fetcher_apis(config.C_MAPI_PATH):
            if mfa!=i:
                self.movie_fetcher_apis_options.append(i)
        #print config.C_MOVIE_FETCHER_API_PATH
        
        #print self.movie_fetcher_apis_options
        
        self.movie_fetcher_apis=SWItem("Movie's Api: ",self.movie_fetcher_apis_options,self.movie_fetcher_apis_callback,self)
        self.movie_fetcher_apis.setToolTip(tool_tip["movie_api"])
        self.advanced_tab_container.addWidget(self.movie_fetcher_apis)
        

        #for i in range(100):
        #    self.advanced_tab_container.addWidget(qg.QPushButton(str(i)))
        #self.advanced_tab
        self.tab_widget.addTab(self.basic_tab, "Basic")
        self.tab_widget.addTab(self.advanced_tab, "Advanced")
        #scrollArea = qg.QScrollArea()
        #scrollArea.setBackgroundRole(qg.QPalette.Dark)
        #scrollArea.setWidget(self.advanced_tab)        

        


        
        ## End Basic ##
        
        
        ##Start Advanced
        #self.make_box_line_edit("Copy Command:", self.advanced_tab_container)
        
        #button1 = QtGui.QPushButton("button1")
        #self.basic_tab_container.addWidget(button1)
        
        
        
        
        self.basic_tab_container.addItem(self.block)
        self.advanced_tab_container.addItem(self.block)

        
        
        self.main_container = QtGui.QVBoxLayout()
        self.main_container.addWidget(self.tab_widget)
        
        self.status_bar=qg.QLabel("",self)
        self.status_bar.setMinimumHeight(20)
        self.status_bar.hide()
        self.status_bar.setContentsMargins(5,5,5,5)
        self.status_bar.setStyleSheet("""
        QLabel{
            background-color: black;
            color:white;
            }
        """)
        
        self.status_bar.setObjectName("status_bar")
        #self.status_bar.setStyleSheet(style)
        #self.status_bar.show()
        self.main_container.setSpacing(0)
        self.main_container.setContentsMargins(0,0,0,0)
        self.main_container.addWidget(self.status_bar)
        
        self.setLayout(self.main_container)
        self.status_timer=qc.QTimer()
        self.status_timer_counter=0
        self.timer=3
        self.status_timer.timeout.connect(self.timeout)


    def add_status(self,msg,timer=5):
        self.status_time_counter=0
        self.timer=timer
        self.status_timer.start(1000)
        self.status_bar.show()
        self.status_bar.setText(msg)
    
    def timeout(self):
        self.status_timer_counter=self.status_timer_counter+1
        #print self.status_timer_counter
        if self.status_timer_counter>=self.timer:
            self.status_bar.setText("")
            self.status_bar.hide()
            self.status_timer.stop()
            self.timer=3











    def send_to_callback(self,*kwards,**kwargs):
        #print "Movie Fetcher Apis CallBack"
        try:
            index=kwards[0]
            msg=self.send_to_options[index]
            self.option.replace("send_to",msg)
            self.add_status("Send To Type: "+msg+" Saved",5)
            
        except Exception,e:
            self.add_status(str(e),5)

    def movie_fetcher_apis_callback(self,*kwards,**kwargs):
        #print "Movie Fetcher Apis CallBack"
        try:
            index=kwards[0]
            msg=self.movie_fetcher_apis_options[index]
            self.option.replace("movie_api",msg)
            self.add_status("Movie's Api: "+msg+" Saved",5)
            
        except Exception,e:
            self.add_status(str(e),5)
        
    def title_style_callback(self,*kwards,**kwargs):
        #print "Title Style Callback"
        try:
            text=self.title_style.edit.text()
            self.option.replace("title_style",text)
            self.add_status("Title Style Saved")
            self.title_style.button.setEnabled(False)
                
        except Exception,e:
            self.add_status(str(e))

    def copy_command_callback(self,*kwards,**kwargs):
        #print "Title Style Callback"
        try:
            text=self.copy_command.edit.text()
            self.option.replace("copy_command",text)
            self.add_status("Copy Command Saved")
            self.copy_command.button.setEnabled(False)
        except Exception,e:
            self.add_status(str(e))
                
    def auto_delete_click(self,*kwards,**kwargs):
        try:
            index=kwards[0]
            msg=self.auto_delete_options[index]
            self.option.replace("auto_delete",msg)
            self.add_status("Auto Delete: "+msg)
            self.mainwindow.imd.movie_remover.auto_delete=msg
        except Exception,e:
            self.add_status(str(e))
                         
    def auto_scan_click(self,*kwards,**kwargs):
        try:
            index=kwards[0]
            msg=self.auto_scan_options[index]
            self.option.replace("auto_scan",msg)
            self.add_status("Auto Scan: "+msg)
            self.mainwindow.imd.movie_adder.auto_scan=msg
        except Exception,e:
            self.add_status(str(e))
            
                   
    def cover_dir_click(self,*kwards,**kwargs):
        #print "Cover Dir click"
        try:
            index=kwards[0]
            msg=self.cover_dir_options[index]
            if msg.lower()=="custom directory":
                        dialog=qg.QFileDialog()
                        dialog.setWindowIcon(qg.QIcon(config.appicon("imovman")))
                        #dialog.setFileMode(qg.QFileDialog.ExistingFiles)
                        dialog.setFileMode(qg.QFileDialog.Directory)
                        dialog.setOption(qg.QFileDialog.ShowDirsOnly)
                        #dialog.setFileMode(QFileDialog::ExistingFiles);
                        try:home=self.option.get_option("cover_dir_custom")
                        except:home=None
                        if home!=None:dialog.setDirectory(home)
                        #dialog.setFilter(QDir.Files);
                        dialog.setWindowTitle("Cover Directory")
                        #dialog.setNameFilter("Theme(*.imt)");
                        if dialog.exec_():
                            msg1=dialog.selectedFiles()[0]
                            self.option.replace("cover_dir_custom",msg1)
                            self.option.replace("cover_dir",msg)
                            self.cover_dir_custom.setText(msg1)
                            self.cover_dir_custom.show()
                            
                            self.add_status("Cover Directory: "+msg)
            else:
                self.option.replace("cover_dir",msg)
                self.cover_dir_custom.hide()
                #self.option.replace("cover_dir_custom", "")
                try:self.option.delete(option_name="cover_dir_custom")
                except:pass
                self.add_status("Cover Directory: "+msg)
                
            
            
        except Exception,e:
            self.add_status(str(e))
            
    def data_dir_click(self,*kwards,**kwargs):
        try:
            index=kwards[0]
            msg=self.data_dir_options[index]
            if msg.lower()=="custom directory":
                        dialog=qg.QFileDialog()
                        dialog.setWindowIcon(qg.QIcon(config.appicon("imovman")))
                        #dialog.setFileMode(qg.QFileDialog.ExistingFiles)
                        dialog.setFileMode(qg.QFileDialog.Directory)
                        dialog.setOption(qg.QFileDialog.ShowDirsOnly)
                        #dialog.setFileMode(QFileDialog::ExistingFiles);
                        try:home=self.option.get_option("data_dir_custom")
                        except:home=None
                        if home!=None:dialog.setDirectory(home)
                        #dialog.setFilter(QDir.Files);
                        dialog.setWindowTitle("Data Directory")
                        #dialog.setNameFilter("Theme(*.imt)");
                        if dialog.exec_():
                            msg1=dialog.selectedFiles()[0]
                            self.option.replace("data_dir_custom",msg1)
                            self.option.replace("data_dir",msg)
                            self.data_dir_custom.setText(msg1)
                            self.data_dir_custom.show()
                            
                            self.add_status("Text Data Directory: "+msg)
            else:
                self.option.replace("data_dir",msg)
                self.data_dir_custom.hide()
                #self.option.replace("cover_dir_custom", "")
                try:self.option.delete(option_name="data_dir_custom")
                except:pass
                self.add_status("Text Data Directory: "+msg)
                
            
            
        except Exception,e:
            self.add_status(str(e))
              
    def cfont(self,clabel,size,bold=False):
        cname_font=clabel.font()
        cname_font.setPointSize(size)
        cname_font.setBold(bold)
        clabel.setFont(cname_font)
        
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    
    def cshow(self):
        self.center()
        self.show()
        
    def chide(self):
        self.hide()



class Test(qg.QWidget):
    def __init__(self):
        super(Test,self).__init__()
        self.hide()
        self.setObjectName("SettingsWindow")
        #self.setStyleSheet(style)
        #self.setSpacing(0)
        self.setContentsMargins(0,0,0,0)
        ## Non Gui ##
        try:self.option=Option()
        except:self.option=None        
        
        self.setWindowFlags(qc.Qt.WindowTitleHint|qc.Qt.WindowCloseButtonHint)
        self.setWindowTitle(config.APP_NAME+" ::: "+"Settings")
        self.icon=appicon("imovman")
        self.setWindowIcon(qg.QIcon(self.icon))
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setFixedSize(500,500)
        elist=qg.QListWidget()
        elist.setContentsMargins(0,0,0,0)
        #elist.setFixedSize(500,500)
        lay=qg.QHBoxLayout()
        lay.setContentsMargins(0,0,0,0)
        #lay.SetFixedSize(500,500)
        #gr=qg.QSizeGrip(list)#;//to resize the widget
        scroll=qg.QScrollArea()
        #scroll.setFixedSize(500,500)
        scroll.setWidget(SettingsWindow())
        #scroll.setHorizontalScrollBarPolicy()
        scroll.setAlignment(qc.Qt.AlignLeft)
        #scroll->setWidgetResizable(true);
        scroll.setBackgroundRole(qg.QPalette.Dark)#;// set background of scroll Area
        #//win=new QWidget();
        for i in range(1,1000):
            qg.QListWidgetItem(str(i),elist)#;//adding items to list
        #lay.addWidget(elist);
        
        lay.addWidget(scroll)
        
        
        self.setLayout(lay)#;//setting layout
        #showMaximized();
        



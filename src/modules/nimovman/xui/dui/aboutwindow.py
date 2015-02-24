'''
Created on Aug 3, 2013

@author: KaWsEr
'''
import webbrowser
from modules.nimovman.xui.core import CoreMiniWindow
from modules.nimovman.core import config,util

from PySide import QtGui
from PySide import QtCore

qg=QtGui
qc=QtCore

class AboutWidget(CoreMiniWindow):
    def __init__(self,*kwards,**kwargs):
        super(AboutWindow,self).__init__()
        self.setWindowTitle("About")



class AboutWindow(QtGui.QWidget):
    def __init__(self):
        super(AboutWindow,self).__init__(None)
        self.setWindowTitle("About "+config.APP_NAME+" "+config.APP_VERSION)
        self.setWindowIcon( qg.QIcon(config.appicon("iMovMan")) )
        self.setStyleSheet(".QWidget.AboutWindow {background:white;}")
        self.setFixedSize(450,350)
        #self.setModal(True)
        
        self.box=qg.QVBoxLayout()
        
        #name
        cname=qg.QLabel(self)
        cname_font=cname.font()
        cname_font.setPointSize(20)
        cname_font.setBold(True)
        cname.setFont(cname_font)
        cname.setText(config.APP_NAME)
        #version
        cversion=qg.QLabel(self)
        cversion_font=cversion.font()
        cversion_font.setPointSize(10)
        cversion.setFont(cversion_font)
        data=util.form_dict(config.BUILD_FILE)
        cvt="Version : %s\n"%config.APP_VERSION
        if data.has_key("buildname"):
            cvt=cvt+"Build Name: %s\n"%data["buildname"]
        if data.has_key("buildnumber"):
            cvt=cvt+"Build Number: %s\n"%data["buildnumber"]
            
            
        cversion.setText(cvt)

        

        cdev=qg.QLabel(self)
        cdev_font=cdev.font()
        cdev_font.setPointSize(12)
        cdev.setFont(cdev_font)
        cdev.setText("Developer : "+config.APP_DEVELOPER)
        
        cdes=qg.QTextBrowser(self)
        cdes.setStyleSheet("border:0px;")
        #cdes.setMaximumHeight(50)
        cdes_font=cdes.font()
        cdes_font.setPointSize(10)
        cdes.setFont(cdes_font)
        cdes.setHtml(config.APP_DESCRIPTION)
        
        ccredits=qg.QTextBrowser(self)
        ccredits.setOpenExternalLinks(True)
        ccredits.setStyleSheet(".QTextBrowser{border:0px;}")
        ccredits_font=ccredits.font()
        ccredits_font.setPointSize(10)
        ccredits.setFont(ccredits_font)
        ccredits.setHtml(config.APP_CREDITS)
        
        
        ccopyright=qg.QLabel(self)
        ccopyright_font=ccopyright.font()
        ccopyright_font.setPointSize(10)
        ccopyright_font.setBold(True)
        ccopyright.setFont(ccopyright_font)
        ccopyright.setText("<center>"+config.APP_COPYRIGHT+"</center>")
        
        spacer=qg.QSpacerItem(450,30)
        
        
        self.button_box=qg.QHBoxLayout()
        self.button_box.addItem(spacer)
        btn_style="""
            .QPushButton {
                border:2px solid #8f8f91;
                border-radius: 5px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);
                min-width: 50px;
                max-width:50px;
                max-height:30px;
                }
            
            .QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #dadbde, stop: 1 #f6f7fa);
                }
            
            .QPushButton:flat {
                border: none; /* no border for a flat push button */
                }
            
            .QPushButton:default {
                border-color: navy; /* make the default button prominent */
                }
        

        """
        ok=qg.QPushButton("OK")
        ok.setStyleSheet(btn_style)
        ok.clicked.connect(self.ok)
        
        visit=qg.QPushButton("Visit")
        visit.setStyleSheet(btn_style)
        visit.clicked.connect(self.visit)
        self.button_box.addWidget(visit)
        self.button_box.addWidget(ok)
        #self.box.addWidget(ok)
        
        self.box.addWidget(cname)
        self.box.addWidget(cversion)
        self.box.addWidget(cdev)
        self.box.addWidget(cdes)
        self.box.addWidget(ccredits)
        self.box.addWidget(ccopyright)
        
        self.box.addLayout(self.button_box)
        self.setLayout(self.box)
        self.hide()
        
        self.setWindowFlags(qc.Qt.CustomizeWindowHint | qc.Qt.WindowTitleHint | qc.Qt.WindowCloseButtonHint | qc.Qt.WindowStaysOnTopHint)
        
    def ok(self):self.hide()
    def visit(self):webbrowser.open(config.APP_WEB)
    def closeEvent(self,evnt):
        self.hide()
        evnt.ignore()
'''
Created on Aug 2, 2013

@author: KaWsEr
'''
from PySide.QtGui import QWidget,QIcon,QVBoxLayout
from PySide.QtCore import Qt
from modules.nimovman.core.config import appicon


class AboutWindow(QWidget):
    def __init__(self):
        super(AboutWindow,self).__init__(None)
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(appicon("iMovMan")) )
        #self.setStyleSheet("QWidget.AboutWidget {background:white;}")
        self.setFixedSize(450,350)
        
        
        #self.box=qg.QVBoxLayout()
        
        #name
        #cname=qg.QLabel(self)
        #cname_font=cname.font()
        #cname_font.setPointSize(20)
        #cname_font.setBold(True)
        #cname.setFont(cname_font)
        #cname.setText(config.APP_NAME)
        #version
        #cversion=qg.QLabel(self)
        #cversion_font=cversion.font()
        #cversion_font.setPointSize(12)
        #cversion.setFont(cversion_font)
        #cversion.setText("Version : "+config.APP_VERSION)

        

        #cdev=qg.QLabel(self)
        #cdev_font=cdev.font()
        #cdev_font.setPointSize(12)
        #cdev.setFont(cdev_font)
        #cdev.setText("Developer : "+config.APP_DEVELOPER)
        
        #cdes=qg.QTextBrowser(self)
        #cdes.setStyleSheet("border:0px;")
        #cdes.setMaximumHeight(50)
        #cdes_font=cdes.font()
        #cdes_font.setPointSize(10)
        #cdes.setFont(cdes_font)
        #cdes.setHtml(config.APP_DESCRIPTION)
        
        #ccredits=qg.QTextBrowser(self)
        #ccredits.setOpenExternalLinks(True)
        #ccredits.setStyleSheet("border:0px;")
        #ccredits_font=ccredits.font()
        #ccredits_font.setPointSize(10)
        #ccredits.setFont(ccredits_font)
        #ccredits.setHtml(config.APP_CREDITS)
        
        
        #ccopyright=qg.QLabel(self)
        #ccopyright_font=ccopyright.font()
        #ccopyright_font.setPointSize(10)
        #ccopyright_font.setBold(True)
        #ccopyright.setFont(ccopyright_font)
        #ccopyright.setText("<center>"+config.APP_COPYRIGHT+"</center>")
        
        #spacer=qg.QSpacerItem(450,30)
        
        
        #self.button_box=qg.QHBoxLayout()
        #self.button_box.addItem(spacer)
        self.hide()
        
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
    def closeEvent(self,evnt):
        self.hide()
        evnt.ignore()

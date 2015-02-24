'''
Created on Aug 19, 2013

@author: KaWsEr
'''

import string
from PySide import QtGui,QtCore
from modules.nimovman.core.dbmodel import Movie

from modules.nimovman.core import config
from modules.nimovman.core import standardsignal


TagUpdated=standardsignal.Signal()
TagUpdates=standardsignal.SignalUnicode()
class TagEditor(QtGui.QDialog):

    def __init__(self,vparent,path):
        super(TagEditor,self).__init__(None)
        self.setModal(True)
        self.path=path
        movieo=Movie()
        movie=movieo.get(path=self.path)[0]
        tags=movie.tags
        preserved_tags=["favourite","wish List","watched"]
        self.found_tags=[]
        
        if tags!="":tags=tags.split(",")
        else:tags=[]
        
        tags=map(string.strip,tags)
        
        tags=map(string.lower,tags)
        for i in preserved_tags:
            if i.lower() in tags:
                self.found_tags.append(i)
                try:
                    del tags[tags.index(i)]
                except:pass
        
        
        tags=",".join(tags)
        self.setWindowIcon( QtGui.QIcon(config.appicon("iMovMan")) )
        self.setWindowTitle("iMovMan ::: Tag Editor")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint )
        self.setFixedSize(500,400)
        self.main_layout=QtGui.QVBoxLayout()
        
        self.tag_edit = QtGui.QTextEdit(self)
        self.tag_edit.setAcceptRichText(False)
        #self.tag_edit.setFixedWidth(500)
        #self.tag_edit.setF
        self.tag_edit.setText(tags)
        
        label=QtGui.QLabel("Enter Tags ( Separated By Comma) :",self)
        self.main_layout.addWidget(label)
        tag_box=QtGui.QVBoxLayout()
        tag_box.addWidget(self.tag_edit)
        self.save=QtGui.QPushButton("Save",self)
        self.save.clicked.connect(self.save_tags)
        self.save.setEnabled(False)
        
        #tag_box.addWidget(self.save)
        
        button_box=QtGui.QHBoxLayout()
        button_box.addItem(QtGui.QSpacerItem(500,2))
        button_box.addWidget(self.save)
        self.main_layout.addLayout(tag_box)
        
        #self.tag_list=QtGui.QListView(self)
        
    
        #self.main_layout.addWidget(self.tag_list)
        self.logViewer = QtGui.QTextBrowser(self)
        self.logViewer.setMaximumHeight(100)
        self.main_layout.addWidget(self.logViewer)
        self.main_layout.addLayout(button_box)
        #self.main_layout.addWidget(self.tag_edit)
        
        
        self.setLayout(self.main_layout)
        
        
        self.tag_edit.textChanged.connect(self.text_changed)
    
    def text_changed(self):
        self.save.setEnabled(True)
        
    def save_tags(self):
        self.add_msg("Saving Tags....")
        self.save.setEnabled(False)
        tags=self.tag_edit.toPlainText()
        if tags=="":tags=[]
        else:tags=tags.split(",")
        
        tags=map(string.strip,tags)
        tags=map(string.lower,tags)
        tags=tags+self.found_tags
        
        tags=list(set(tags))
        #print tags
        tags=",".join(tags)
        #print tags
        try:
            movieo=Movie()
            data={}
            data["path"]=self.path
            data["tags"]=tags
            if movieo.update(data):
                self.add_msg("Tags Updated..")
                try:
                    TagUpdated.signal.emit()
                    TagUpdates.signal.emit(self.path)
                except:
                    pass
            else:
                self.add_msg("Failed to update tags")
                self.save.setEnabled(True)
        except Exception,e:
            self.add_msg("Error: %s"%e)
        #print tags
    def add_msg(self,msg):
        self.logViewer.append(msg)
        vs=self.logViewer.verticalScrollBar()
        vs.setValue(vs.maximum())
        #self.logViewer.scroll(100,100)
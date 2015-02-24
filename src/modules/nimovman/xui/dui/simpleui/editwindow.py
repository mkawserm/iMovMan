'''
Created on Aug 20, 2013

@author: KaWsEr
'''

from PySide import QtCore,QtGui
from modules.nimovman.core import util
from modules.nimovman.core import config
from modules.nimovman.core.dbmodel import Movie
from modules.nimovman.core import standardsignal

MovieEditorUpdated=standardsignal.SignalUnicode()
class MovieEditor(QtGui.QDialog):
    def __init__(self,path):
        super(MovieEditor,self).__init__(None)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | 
                            QtCore.Qt.WindowCloseButtonHint | 
                            QtCore.Qt.WindowMinimizeButtonHint | 
                            QtCore.Qt.WindowMaximizeButtonHint)
        self.path=path
        
        self.boxes={}
        try:
            movieo=Movie()
            movie=movieo.get(path=path)[0]
            self.data=movieo.map_single(movie)
        except:
            self.data=None
        self.setFixedSize(500,500)
        self.setWindowIcon(QtGui.QIcon(config.appicon("iMovMan")))
        name=util.get_name_from_path(path)
        self.setWindowTitle(name+" ::: MovieEditor")
        #print data
        
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(5)
        
        for i in config.MOVIE_DB_KEYS:
            self.edit_line_box(str(i), layout)
        widget = QtGui.QWidget()
        widget.setLayout(layout)
        area = QtGui.QScrollArea()
        area.setWidget(widget)
        layout2 = QtGui.QVBoxLayout()
        layout2.addWidget(area)
        
        self.save=QtGui.QPushButton("Save")
        self.save.clicked.connect(self.save_data)
        self.logViewer = QtGui.QTextBrowser(self)
        self.logViewer.setMaximumHeight(100)
                

        layout2.addWidget(self.logViewer)

        layout2.addWidget(self.save)
                
        self.setLayout(layout2)
        area.setWidgetResizable(True)
        self.add_msg("<b><font color=red>** Genre,Actors,Director,Writer Must be separated with comma</font></b>")
        self.add_msg("<b>**Poster Field is the Image web url not your hard disk image</b>")
        self.save.setEnabled(False)

    
    
    def enable_save(self,*kwards,**kwargs):
        self.save.setEnabled(True)
        
    def save_data(self):
        #print self.boxes
        self.add_msg("Saving..")
        self.save.setEnabled(False)
        ndata={}
        for key in self.boxes.keys():
            if key=="plot":
                ndata[key]=self.boxes[key].toPlainText()
            else:
                ndata[key]=self.boxes[key].text()
        try:
            ndata["path"]=self.path
            movieo=Movie()
            if movieo.update(ndata):
                self.add_msg("Movie Updated")
                MovieEditorUpdated.signal.emit(self.path)
            else:
                self.add_msg("Failed to update data")
                self.save.setEnabled(True)
        except Exception,e:
            self.add_msg("Failure %s"%e)
        
    def edit_line_box(self,title,main):
        layout=QtGui.QHBoxLayout()
        label=QtGui.QLabel(title+": ")
        e=QtGui.QTextEdit()
        e.toPlainText()

        if title.lower()=="plot":
            edit=QtGui.QTextEdit(unicode(self.data[title.lower()]))
            #edit.textEdited.connect(self.enable_save)
            edit.textChanged.connect(self.enable_save)
            edit.setFixedHeight(150)
        else:
            edit=QtGui.QLineEdit(unicode(self.data[title.lower()]))
            edit.setFixedHeight(30)
            edit.textEdited.connect(self.enable_save)
        
        edit.setMinimumWidth(300)
        layout.addWidget(label)
        layout.addWidget(edit)
        self.boxes[title.lower()]=edit
        
        #self.box_layout.addWidget(edit)
        main.addLayout(layout)
        
    def add_msg(self,msg):
        self.logViewer.append(msg)
        vs=self.logViewer.verticalScrollBar()
        vs.setValue(vs.maximum())
        #self.logViewer.scroll(100,100)
        
        
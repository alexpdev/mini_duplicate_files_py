import os
from os.path import dirname
import sys
import hashlib
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

hashing = lambda x: hashlib.sha1(x.read_bytes()).hexdigest()

class Window(QMainWindow):
    def __init__(self,app,parent=None):
        super().__init__(parent=parent)
        self.app = app
        self.central = CentralWidget(parent=self)
        self.centLayout = QVBoxLayout()
        self.central.setLayout(self.centLayout)
        self.hlayout1 = QHBoxLayout()
        self.button1 = QPushButton(parent=self.central)
        self.button2 = QPushButton(parent=self.central)
        self.button1.setText("Choose Folders")
        self.button2.setText("Find Duplicates")
        self.button1.pressed.connect(self.choose_file)
        self.button2.pressed.connect(self.find_duplicates)
        self.hlayout1.addWidget(self.button1)
        self.hlayout1.addWidget(self.button2)
        self.centLayout.addLayout(self.hlayout1)
        self.fsdialog = QFileDialog(parent=self.central)
        self.list1 = QListWidget(parent=self.central)
        self.list2 = QListWidget(parent=self.central)
        self.list3 = QListWidget(parent=self.central)
        self.centLayout.addWidget(self.list1)
        self.centLayout.addWidget(self.list2)
        self.centLayout.addWidget(self.list3)
        self.setCentralWidget(self.central)
        self.setWindowTitle("Duplicate Explorer")
        self.fsdialog.setFileMode(QFileDialog.FileMode(2))
        self.fsdialog.setAcceptMode(QFileDialog.AcceptMode(0))
        self.fsdialog.setOptions(QFileDialog.Options(1))
        self.dirs = []

    def choose_file(self):
        path = self.fsdialog.getExistingDirectory(caption="Directory",directory="/")
        c = self.list1.count()
        self.list1.insertItem(c,str(path))
        path = Path(path)
        self.dirs.append(path)

    def find_duplicates(self):
        lex,dups = {},set()
        for path in self.dirs:
            self.walk_dir(path,lex,dups)
        parents = {}
        for path in dups:
            dname = dirname(path)
            if dname not in parents:
                parents[dname] = [1 , len(os.listdir(dname))]
            else:
                parents[dname][0] = parents[dname][0] + 1
        for k,v in parents.items():
            c = self.list3.count()
            self.list3.insertItem(c,f"{v[0]} of {v[1]} files are duplicates in {k}")




    def add_list2_item(self,text):
        c = self.list2.count()
        self.list2.insertItem(c,text)

    def walk_dir(self,path,lex,dups):
        for item in path.iterdir():
            if item.is_file():
                if item.name not in lex:
                    lex[item.name] = [0,str(item)]
                else:
                    lexitem = lex.get(item.name)
                    hash1 = hashing(item)
                    if not lexitem[0]:
                        hash2 = hashing(Path(lexitem[1]))
                        lexitem[0] = hash2
                        if hash1 == hash2:
                            lexitem.append(str(item))
                            dups.add(str(item))
                            dups.add(lexitem[1])
                            self.add_list2_item(lexitem[1])
                            self.add_list2_item(str(item))
                    elif lexitem[0] == hash1:
                        dups.add(str(item))
                        self.add_list2_item(str(item))
                        lexitem.append(str(item))
            else:
                self.walk_dir(item,lex,dups)





class CentralWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setObjectName("central")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window(app)
    win.show()
    sys.exit(app.exec())

import os
import config
from PySide6.QtWidgets import QSizePolicy, QTreeWidget, QTreeWidgetItem, QLabel, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QDir
from PySide6.QtGui import QIcon

class FileBrowserWidget(QWidget):
    def __init__(self, path=None):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.path_label = QLabel((path if path else os.getcwd()).split("/")[-1])
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)  
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.file_tree)
        self.file_tree.itemExpanded.connect(self.expand_directory)
        self.__current_path: str = None
        
    def populate_tree(self, path, parent):
        directory_icon = QIcon(config.icon_path_folder_open)
        file_icon = QIcon(config.icon_path_file)
        directory = QDir(path)
        directory.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        
        for entry in directory.entryInfoList():
            item = QTreeWidgetItem(parent, [entry.fileName()])
            if entry.isDir():
                item.setIcon(0, directory_icon)
                dummy_child = QTreeWidgetItem()
                dummy_child.setText(0, '')
                item.addChild(dummy_child)
            else:
                item.setIcon(0, file_icon)

    def expand_directory(self, item):
        if item.childCount() == 1 and item.child(0).text(0) == '':
            item.takeChildren()
            parent_path = self.get_item_path(item)
            self.populate_tree(self.__current_path, item)

    def get_item_path(self, item):
        path = []
        while item:
            path.insert(0, item.text(0))
            item = item.parent()
        return os.path.join(self.__current_path, *path)
    
    def set_current_path(self, path: str) -> None:
        self.file_tree.clear()
        self.__current_path = path
        self.populate_tree(path, self.file_tree)

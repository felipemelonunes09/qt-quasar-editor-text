import os
import config
from PySide6.QtWidgets import QSizePolicy, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QLabel
from PySide6.QtCore import QDir, Qt, QMimeData, QFile
from PySide6.QtGui import QIcon, QDrag, QBrush, QColor

from theme.ThemeManager import ThemeManager

class FileBrowserWidget(QTreeWidget):
    def __init__(self, path=None):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.__current_path: str = None
        self.itemExpanded.connect(self.expand_directory)
        self.setHeaderHidden(True)  
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        self.mapper: dict[str, QTreeWidgetItem] = dict()
        
    def populate_tree(self, path, parent):
        directory_icon = QIcon(config.icon_path_folder_open)
        file_icon = QIcon(config.icon_path_file)
        directory = QDir(path)
        directory.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        directory.setSorting(QDir.SortFlag.DirsFirst)
        for entry in directory.entryInfoList():
            item = QTreeWidgetItem(parent, [entry.fileName()])
            item.setForeground(0, QBrush(QColor(ThemeManager.theme['text-color-primary'])))
            if entry.isDir():
                item.setIcon(0, directory_icon)
                dummy_child = QTreeWidgetItem()
                dummy_child.setText(0, '')
                item.addChild(dummy_child)
            else:
                file = QFile(os.path.join(path, entry.fileName()))
                item.setData(0, Qt.UserRole, (file, path, entry.fileName()))
                item.setIcon(0, file_icon)
                self.mapper[file.fileName()] = item
                
    def expand_directory(self, item):
        if item.childCount() == 1 and item.child(0).text(0) == '':
            item.takeChildren()
            parent_path = self.get_item_path(item)
            self.populate_tree(parent_path, item)
            
    def get_item_path(self, item):
        path = []
        while item:
            path.insert(0, item.text(0))
            item = item.parent()
        return os.path.join(self.__current_path, *path)
    
    def set_current_path(self, path: str) -> None:
        self.clear()
        self.__current_path = path
        self.populate_tree(path, self)
        
    def startDrag(self, supported_actions):
        item = self.currentItem()
        if item:
            file, path, name = item.data(0, Qt.UserRole)
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(os.path.join(path, name)) 
            mime_data.setProperty("path", os.path.join(path, name))
            mime_data.setProperty("name", name)
            drag.setMimeData(mime_data)
            drag.exec(Qt.MoveAction)
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QFrame
from core.shared.widgets.FileTab import FileTab
from core.file_objects import File
from PySide6.QtCore import Signal


class FileBar(QFrame):
    closing_current = Signal(File)
    tab_click = Signal(File)
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("FileBar")
        self.setFixedHeight(40)
        self.__tabs: dict[int, QFrame] = dict()
        self.__list: dict[str, File] = dict()
        self.__layout = QHBoxLayout(self)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.__layout.addStretch()
        self.__current_file: File = None
        self.setLayout(self.__layout)
        self.update()
        
    def get_current_file(self) -> File:
        return self.__current_file
        
    def addFile(self, file: File, current=False) -> None:
        if not file.get_path() in self.__list: 
            self.__remove_current_from_all()
            tab = self.__create_tab(file)
            self.__tabs[id(file)] = tab
            self.__layout.addWidget(tab)
            self.__list[file.get_path()] = file
            self.__current_file = file if current else None
            tab.setObjectName("CurrentFileTab") if current else tab.setObjectName("FileTab")
        else:
            file = self.__list.get(file.get_path(), None)
            if current and file:
                self.__current_file = file
            
    def removeFile(self, file: File) -> None:
        if file.get_path() in self.__list:
            self.__tabs[id(file)].deleteLater() 
            del self.__tabs[id(file)]
            self.__list[file.get_path()] = None
            del self.__list[file.get_path()]
    
    def set_current_file_edited(self):
        if self.__current_file:
            self.__current_file.set_edited(True)
            self.__tabs[id(self.__current_file)].setStyleSheet("QLabel { color: lightgreen; }")
    
    def __remove_current_from_all(self):
        for tab_id in self.__tabs:
            self.__tabs[tab_id].setObjectName("FileTab")
            self.__tabs[tab_id].style().polish(self.__tabs[tab_id])
    
    def __on_tab_close(self, file: File):
        self.removeFile(file)
        if self.__current_file:
            if file.get_path() == self.__current_file.get_path():
                next_id = next(iter(self.__list), None)
                next_file = self.__list.get(next_id, None)
                self.closing_current.emit(next_file)
                self.__current_file = self.__list.get(next_file)
        else:
            self.closing_current.emit(None)
    
    def __create_tab(self, file: File) -> QFrame:
        tab = FileTab(self, file, clickcallback=self.tab_click.emit)
        tab.x_button.clicked.connect(lambda: self.__on_tab_close(file))
        return tab
